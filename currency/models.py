# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import uuid
from datetime import datetime

from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext as _

from accounts.models import Account, Provider, Consumer
from currency.exceptions import AllInvitesSent
from currency_server import create_account
from helpers import send_template_email
from simple_bpm.models import ProcessWorkflow, CurrentProcess, CurrentProcessStep, ProcessWorkflowEvent

MAX_INVITATIONS_PER_USER = 5
INVITE_DURATION_MONTHS = 3

class InvitationsManager(models.Manager):

    def pending(query, entity=None):
        return query.filter(workflow__completed=False)

    def is_valid_token(self, token):
        invite = GuestInvitation.objects.filter(token=token).first()
        return invite is not None and (invite.used == False or invite.single_use == False)

    def invite_user(self, account, email):

        invitations_used = GuestInvitation.objects.filter(invited_by=account, used=True).count()
        if invitations_used >= MAX_INVITATIONS_PER_USER:
            print 'User used all her invites!'
            raise AllInvitesSent(invitations_used)
        else:
            invitation = self.create(invited_by=account, token=uuid.uuid4())
            invitation.send_email(email)
            return invitation



class GuestInvitation(models.Model):

    invited_by = models.ForeignKey(Account, null=False, related_name='invitations', verbose_name=_('Invitado por'))
    token = models.CharField(max_length=40, verbose_name=_('Token'))
    used = models.BooleanField(default=False, verbose_name=_('Utilizado'))
    single_use = models.BooleanField(default=True, verbose_name=_('De un solo uso'))

    objects = InvitationsManager()

    class Meta:
        verbose_name = _('Invitacion')
        verbose_name_plural = _('Invitaciones')


    def send_email(self, email):
        send_template_email(
            title='Invitación al Mercado Social de Madrid',
            destination=email,
            template_name='guest_invite',
            template_params={ 'token':self.token, 'invited_by':self.invited_by.display_name }
        )

    def __unicode__(self):
        return self.token



class GuestAccount(models.Model):

    invited_by = models.ForeignKey(Account, null=False, related_name='invited_guests', verbose_name=_('Invitada por'))
    active = models.BooleanField(default=True, verbose_name=_('Activa'))
    cif = models.CharField(max_length=30, null=False, blank=False, verbose_name=_('NIF/CIF'), unique=True)
    first_name = models.CharField(null=True, blank=True, max_length=250, verbose_name=_('Nombre'))
    last_name = models.CharField(null=True, blank=True, max_length=250, verbose_name=_('Apellidos'))

    contact_phone = models.CharField(max_length=50, null=True, blank=True, verbose_name=_('Teléfono de contacto'))
    contact_email = models.EmailField(null=False, verbose_name=_('Email de contacto'))
    address = models.TextField(null=True, blank=True, verbose_name=_('Dirección'))
    city = models.CharField(null=True, blank=True, max_length=250, verbose_name=_('Municipio'))
    province = models.CharField(null=True, blank=True, max_length=100, verbose_name=_('Provincia'))
    postalcode = models.CharField(null=True, blank=True, max_length=10, verbose_name=_('Código Postal'))

    registration_date = models.DateField(verbose_name=_('Fecha de alta'), null=True, blank=True)
    expiration_date = models.DateField(verbose_name=_('Fecha de caducidad'), null=True, blank=True)


    class Meta:
        verbose_name = _('Invitada')
        verbose_name_plural = _('Invitadas')
        permissions = (
            ("mespermission_can_view_guests", _("Puede ver la lista de invitadas")),
        )

    @property
    def template_prefix(self):
        return 'guest'

    @property
    def display_name(self):
        return "{} {}".format(self.first_name, self.last_name)

    def __str__(self):
        return self.display_name


class CurrencyAppUsersManager(models.Manager):

    def create_app_invited_user(self, guest_account):

        user = self.create(is_guest=True, cif=guest_account.cif, guest_account=guest_account)
        result = create_account.post_guest(guest_account)
        user.is_pushed = result
        user.save()

    def create_app_user(self, account):

        user = self.create(cif=account.cif, account=account)

        if account.get_real_instance_class() is Provider:
            result = create_account.post_entity(account)
            user.is_pushed = result
            user.save()

        if account.get_real_instance_class() is Consumer:
            result = create_account.post_consumer(account)
            user.is_pushed = result
            user.save()


class CurrencyAppUser(models.Model):
    is_guest = models.BooleanField(default=False, verbose_name=_('Es invitada'))
    is_pushed = models.BooleanField(default=False, verbose_name=_('Actualizado en el servidor'))
    cif = models.CharField(max_length=30, verbose_name=_('NIF/CIF'))
    username = models.CharField(null=True, max_length=50, verbose_name=_('Nombre de usuario'))
    uuid = models.UUIDField(null=True, verbose_name=_('Identificador único'))

    account = models.ForeignKey(Account, null=True, verbose_name=_('Socia'), related_name='app_user')
    guest_account = models.ForeignKey(GuestAccount, null=True, verbose_name=_('Invitada'), related_name='app_user')

    objects = CurrencyAppUsersManager()



# Method to add every user with a related person to the persons group
@receiver(post_save, sender=GuestAccount)
def add_user_to_group(sender, instance, created, **kwargs):

    if created:
        print 'Creating app user'
        CurrencyAppUser.objects.create_app_invited_user(instance)

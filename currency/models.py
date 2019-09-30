# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import uuid
from datetime import datetime

import dateutil
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
        if not token:
            return False
        invite = GuestInvitation.objects.filter(token=token).first()
        return invite is not None and (invite.used == False or invite.single_use == False)

    def invite_user(self, account, email):

        invitations_used = GuestInvitation.objects.filter(invited_by=account, used=True).count()
        if invitations_used >= MAX_INVITATIONS_PER_USER:
            print('User used all her invites!')
            raise AllInvitesSent(invitations_used)
        else:
            invitation = self.create(invited_by=account, token=uuid.uuid4())
            invitation.send_email(email)
            return invitation



class GuestInvitation(models.Model):

    invited_by = models.ForeignKey(Account, null=True, blank=True, related_name='invitations', verbose_name=_('Invitado por'), on_delete=models.CASCADE)
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

    invited_by = models.ForeignKey(Account, null=True, blank=True, related_name='invited_guests', verbose_name=_('Invitada por'), on_delete=models.SET_NULL)
    token_used = models.ForeignKey(GuestInvitation, null=True, blank=True, related_name='invited_guests', verbose_name=_('Token utilizado'), on_delete=models.SET_NULL)
    active = models.BooleanField(default=True, verbose_name=_('Activa'))
    guest_reference = models.CharField(default=uuid.uuid4, null=True, blank=True, max_length=50, verbose_name=_('Referencia invitado'))
    cif = models.CharField(max_length=30, null=True, blank=True, verbose_name=_('NIF/CIF'), unique=True)
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

    cyclos_user = models.CharField(null=True, blank=True, max_length=150, verbose_name=_('Antiguo usuario en Cyclos'))


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

    @property
    def is_active(self):
        return datetime.date.today() < self.expiration_date

    def __str__(self):
        return self.display_name.encode('utf-8')


class CurrencyAppUsersManager(models.Manager):

    def create_app_invited_user(self, guest_account):

        user = self.create(is_guest=True, cif=guest_account.guest_reference, guest_account=guest_account)
        result, uuid = create_account.post_guest(guest_account)
        if result:
            user.is_pushed = result
            user.uuid = uuid
            user.save()

    def create_app_user(self, account):

        user = self.create(cif=account.cif, account=account)
        action = None

        if account.get_real_instance_class() is Provider:
            action = create_account.post_entity
        elif account.get_real_instance_class() is Consumer:
            action = create_account.post_consumer

        if action:
            result, uuid = action(account)
            user.is_pushed = result
            if result:
                user.uuid = uuid
            user.save()



class CurrencyAppUser(models.Model):
    is_guest = models.BooleanField(default=False, verbose_name=_('Es invitada'))
    is_pushed = models.BooleanField(default=False, verbose_name=_('Actualizado en el servidor'))
    cif = models.CharField(max_length=50, verbose_name=_('NIF/CIF'))
    username = models.CharField(null=True, max_length=50, verbose_name=_('Nombre de usuario'))
    uuid = models.UUIDField(null=True, verbose_name=_('Identificador único'))

    account = models.ForeignKey(Account, null=True, blank=True, verbose_name=_('Socia'), related_name='app_user', on_delete=models.CASCADE)
    guest_account = models.ForeignKey(GuestAccount, null=True, blank=True, verbose_name=_('Invitada'), related_name='app_user', on_delete=models.CASCADE)

    objects = CurrencyAppUsersManager()



# Method to create the app user of a guest account
@receiver(post_save, sender=GuestAccount)
def create_user_in_app(sender, instance, created, **kwargs):

    if created:
        instance.registration_date = datetime.now()
        instance.expiration_date = datetime.now() + dateutil.relativedelta.relativedelta(months=INVITE_DURATION_MONTHS)
        CurrencyAppUser.objects.create_app_invited_user(instance)
        instance.save()


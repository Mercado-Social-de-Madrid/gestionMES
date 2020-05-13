# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime

import os
from django.conf import settings
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.utils.translation import gettext as _
from sepaxml import SepaTransfer, SepaDD

from core.models import User
from payments.models import PendingPayment, DEBIT


class SepaPaymentsBatch(models.Model):
    attempt = models.DateTimeField(auto_now_add=True, verbose_name=_('Añadido'))
    amount = models.FloatField(default=0, verbose_name=_('Cantidad total'))
    title = models.CharField(null=True, blank=True, verbose_name=_('Nombre'), max_length=180)
    generated_by = models.ForeignKey(User, null=True, verbose_name=_('Usuario que generó'), on_delete=models.SET_NULL)
    payments = models.ManyToManyField(PendingPayment, through='SepaBatchResult', verbose_name=_('Pagos incluídos'), related_name='sepa_batches')
    sepa_file = models.FileField(null=True, blank=True, upload_to='sepa', verbose_name=_('Fichero SEPA'))

    class Meta:
        verbose_name = _('Remesa SEPA')
        verbose_name_plural = _('Remesas SEPA')
        ordering = ['-generated_by']
        permissions = (
            ("mespermission_can_manage_sepa", _("Puede gestionar remesas de pagos SEPA")),
        )


    def generate_batch(self):
        sepa = SepaDD(settings.SEPA_CONFIG,schema="pain.008.001.02", clean=True)
        payments = []

        for batch_result in SepaBatchResult.objects.filter(batch=self):
            payment = batch_result.payment

            if payment.amount <= 0:
                batch_result.success = False
                batch_result.fail_reason = ZERO_AMOUNT

            if not payment.account or not payment.account.iban_code:
                batch_result.success = False
                batch_result.fail_reason = IBAN_MISSING

            else:
                batch_result.iban_code = payment.account.iban_code[4:8]
                bank = BankBICCode.objects.filter(bank_code=batch_result.iban_code).first()
                if not bank:
                    batch_result.success = False
                    batch_result.fail_reason = BIC_MISSING

            if batch_result.success:
                batch_result.bic_code = bank.bic_code
                batch_result.bank_name = bank.bank_name
                pay = {
                    "name": payment.account.display_name,
                    "IBAN": payment.account.iban_code,
                    "amount": int(payment.amount * 100),
                    "BIC":  batch_result.bic_code,
                    "type": "RCUR",
                    "collection_date": datetime.date.today(),
                    "mandate_id": payment.account.cif,
                    "execution_date": datetime.date.today(),
                    "mandate_date": datetime.date.today(),
                    "description": payment.concept,
                    "endtoend_id": str(payment.reference).replace('-',''),
                }
                sepa.add_payment(pay)
                payments.append(batch_result.payment)

            batch_result.save()

        if (len(payments) > 0):
            sepa_xml = sepa.export(validate=True)
            xml_temp = NamedTemporaryFile()
            xml_temp.write(sepa_xml)
            xml_temp.flush()

            self.sepa_file.save(f"sepa_batch_{self.pk}.xml", File(xml_temp))
            self.save()

            # We check the included payments as paid
            '''for payment in payments:
                payment.completed = True
                payment.timestamp = datetime.datetime.now()
                payment.type = DEBIT
                payment.save()'''


IBAN_MISSING = 1
BIC_MISSING = 2
ZERO_AMOUNT = 3
FAIL_REASONS = (
    (IBAN_MISSING, 'La cuenta no tiene IBAN'),
    (BIC_MISSING, 'Entidad desconocida'),
    (ZERO_AMOUNT, 'La transferencia no tenía una cantidad positiva'),
)


class SepaBatchResult(models.Model):
    batch = models.ForeignKey(SepaPaymentsBatch, related_name='batch_payments', on_delete=models.SET_NULL, null=True)
    payment = models.ForeignKey(PendingPayment, related_name='batch_payments', on_delete=models.SET_NULL, null=True,blank=True)
    success = models.BooleanField(default=True, verbose_name=_('Añadido correctamente'))
    iban_code = models.CharField(null=True, blank=True, verbose_name=_('Código de cuenta'), max_length=20)
    bic_code = models.CharField(null=True, blank=True, verbose_name=_('Código BIC'), max_length=20)
    bank_name = models.CharField(null=True, blank=True, verbose_name=_('Nombre del banco'), max_length=180)
    fail_reason = models.IntegerField(choices=FAIL_REASONS, default=0)


class BankBICCode(models.Model):
    bank_code = models.CharField(null=True, blank=True, verbose_name=_('Código de cuenta'), max_length=20)
    bank_name = models.CharField(null=True, blank=True, verbose_name=_('Nombre del banco'), max_length=180)
    bic_code = models.CharField(null=True, blank=True, verbose_name=_('Código BIC'), max_length=20)
    modified = models.DateTimeField(auto_now=True, verbose_name=_('Última actualización'))

    class Meta:
        verbose_name = _('Código BIC')
        verbose_name_plural = _('Códigos BIC')


@receiver(post_delete, sender=SepaPaymentsBatch)
def delete_batch_file(sender, instance, **kwargs):
    try:
        if instance.sepa_file and instance.sepa_file.storage.exists(instance.sepa_file.name):
            os.remove(instance.sepa_file.path)
    except OSError:
        print("Error deleting SEPA batch file")

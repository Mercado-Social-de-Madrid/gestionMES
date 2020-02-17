# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime

from django.conf import settings
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from django.db import models
from django.utils.translation import gettext as _
from sepaxml import SepaTransfer, SepaDD

from core.models import User
from payments.models import PendingPayment


class SepaBatch(models.Model):
    attempt = models.DateTimeField(auto_now_add=True, verbose_name=_('Añadido'))
    amount = models.FloatField(default=0, verbose_name=_('Cantidad total'))
    title = models.CharField(null=True, blank=True, verbose_name=_('Nombre'), max_length=180)
    generated_by = models.ForeignKey(User, null=True, verbose_name=_('Usuario que generó'), on_delete=models.SET_NULL)
    payments = models.ManyToManyField(PendingPayment, null=True, blank=True, verbose_name=_('Pagos incluídos'), related_name='sepa_batches')
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

        for payment in self.payments.all():
            if not payment.account or not payment.account.iban_code:
                print("No IBAN... passing.")
                continue

            pay = {
                "name": payment.account.display_name,
                "IBAN": payment.account.iban_code,
                "amount": int(payment.amount * 100),
                "BIC": "ETICES21XXX",
                "type": "RCUR",
                "collection_date": datetime.date.today(),
                "mandate_id": "1234",
                "execution_date": datetime.date.today(),
                "mandate_date": datetime.date.today(),
                "description": payment.concept,
                "endtoend_id": str(payment.reference).replace('-',''),
            }
            sepa.add_payment(pay)

        sepa_xml = sepa.export(validate=True)
        xml_temp = NamedTemporaryFile()
        xml_temp.write(sepa_xml)
        xml_temp.flush()

        self.sepa_file.save(f"sepa_batch_{self.pk}.xml", File(xml_temp))
        self.save()

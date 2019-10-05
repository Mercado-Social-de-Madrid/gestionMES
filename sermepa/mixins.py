#-*- coding: utf-8 -*-
import re
import hashlib
import logging
import base64
import json

import hmac
import pyDes

from django.conf import settings

log = logging.getLogger(__name__)


class SermepaMixin(object):

    @staticmethod
    def encode_base64(data):
        return base64.b64encode(data)

    @staticmethod
    def decode_base64(data):
        return base64.b64decode(data)

    @staticmethod
    def urlsafe_b64encode(data):
        return base64.urlsafe_b64encode(data)

    @staticmethod
    def urlsafe_b64decode(data):
        return base64.urlsafe_b64decode(data)

    @classmethod
    def decode_merchant_parameters(cls, merchant_parameters):
        return json.loads(cls.urlsafe_b64decode(str(merchant_parameters)))

    @staticmethod
    def encrypt_3des(message, key):

        des3 = pyDes.triple_des(key, mode=pyDes.CBC, IV='\0' * 8, pad='\0', padmode=pyDes.PAD_NORMAL)
        encrypted = des3.encrypt(str(message).encode('utf8'))
        return encrypted

    def hmac256(self, data, key):
        firma_hmac = hmac.new(key, data, hashlib.sha256).digest()
        return self.encode_base64(firma_hmac)

    def get_firma_peticion(self, merchant_order, merchant_parameters, clave_sha256):
        key = self.decode_base64(clave_sha256)
        key_3des = self.encrypt_3des(merchant_order, key)
        return self.hmac256(merchant_parameters, key_3des)

    def get_firma_respuesta(self, ds_order, ds_merchant_parameters, ds_signature):
        key = self.decode_base64(settings.SERMEPA_SECRET_KEY)
        order_encrypted = self.encrypt_3des(ds_order, key)
        firma = self.hmac256(ds_merchant_parameters.encode(), order_encrypted)

        alphanumeric_characters = re.compile('[^a-zA-Z0-9]')
        ds_dignature_safe = re.sub(alphanumeric_characters, '', ds_signature)
        ds_dignature_calculated_safe = re.sub(alphanumeric_characters, '', firma.decode())
        if ds_dignature_safe == ds_dignature_calculated_safe:
            return True
        else:
            return False

    def verifica_firma(self, ds_order, merchant_parameters, firma, clave_sha256):
        return firma == self.get_firma_respuesta(ds_order, merchant_parameters, clave_sha256)

    @staticmethod
    def operacion_valida(respuesta):
        valor = int(respuesta)
        log.debug('Valor : %s ' % valor)
        return (valor >= 0) and (valor <= 99)

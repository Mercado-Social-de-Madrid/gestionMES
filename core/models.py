# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import gettext as _
from imagekit.models import ProcessedImageField, ImageSpecField
from pilkit.processors import ResizeToFit, ResizeToFill



from helpers import RandomFileName


class User(AbstractUser):
    class Meta:
        verbose_name = _('Usuario')
        verbose_name_plural = _('Usuarios')


class Gallery(models.Model):

    title = models.CharField(null=True, blank=True, verbose_name=_('Título'), max_length=250)
    class Meta:
        verbose_name = _('Galería')
        verbose_name_plural = _('Galerías')


class GalleryPhoto(models.Model):

    gallery = models.ForeignKey(Gallery, null=True, related_name='photos')
    order = models.IntegerField(verbose_name=_('Orden'), default=0)
    title = models.CharField(null=True, blank=True, verbose_name=_('Título'), max_length=250)
    image = ProcessedImageField(null=True, blank=True, upload_to=RandomFileName('photos/'),
                                processors=[ResizeToFit(512, 512, upscale=False)], format='JPEG')

    image_thumbnail = ImageSpecField(source='image',
                                       processors=[ResizeToFill(150, 150, upscale=False)],
                                       format='JPEG',
                                       options={'quality': 70})

    uploaded = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('Foto')
        verbose_name_plural = _('Fotos')
        ordering = ['order']

# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-02-06 12:39
from __future__ import unicode_literals

from django.db import migrations


def create_collabs(apps, schema_editor):
    # We can't import the model directly as it may be a newer
    # version than this migration expects. We use the historical version.
    Entity = apps.get_model('accounts', 'Entity')
    Collaborator = apps.get_model('accounts', 'Colaborator')
    Collaboration = apps.get_model('accounts', 'Collaboration')
    EntityCollaboration = apps.get_model('accounts', 'EntityCollaboration')

    default_collab = Collaboration.objects.create(name="Acuerdo de colaboración")
    collab_collab = Collaboration.objects.create(name="Acuerdo general")
    sponsor_collab = Collaboration.objects.create(name="Patrocinio")

    for collaborator in Collaborator.objects.all():
        entity = Entity.objects.filter(pk=collaborator.pk).first()
        if not entity:
            continue
        if collaborator.is_sponsor:
            EntityCollaboration.objects.get_or_create(entity=entity, collaboration=sponsor_collab)
        if collaborator.is_collaborator:
            EntityCollaboration.objects.get_or_create(entity=entity, collaboration=collab_collab)

        if not collaborator.is_collaborator and not collaborator.is_sponsor:
            EntityCollaboration.objects.get_or_create(entity=entity, collaboration=default_collab)



class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0029_collaboration'),
    ]

    operations = [
        migrations.RunPython(create_collabs),
    ]
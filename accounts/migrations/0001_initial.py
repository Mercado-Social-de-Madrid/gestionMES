# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2019-01-03 15:14
from __future__ import unicode_literals

import datetime
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import helpers.filesystem
import imagekit.models.fields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('activa', 'Activa'), ('pagoinicial', 'Pendiente de pago inicial'), ('pagopendiente', 'Pago de cuota pendiente'), ('anulada', 'Anulada por impago'), ('bsja', 'Baja')], default='activa', max_length=20, verbose_name='Estado')),
                ('cif', models.CharField(max_length=30, unique=True, verbose_name='NIF/CIF')),
                ('contact_phone', models.CharField(blank=True, max_length=50, null=True, verbose_name='Tel\xe9fono de contacto')),
                ('contact_email', models.EmailField(max_length=254, verbose_name='Email de contacto')),
                ('member_type', models.CharField(blank=True, choices=[(b'consumidora', b'Socia consumidora'), (b'colaboradora', b'Socia colaboradora'), (b'proveedora', b'Socia proveedora')], max_length=30, null=True, verbose_name='Tipo de socia')),
                ('address', models.TextField(blank=True, null=True, verbose_name='Direcci\xf3n')),
                ('city', models.CharField(blank=True, max_length=250, null=True, verbose_name='Municipio')),
                ('province', models.CharField(blank=True, max_length=100, null=True, verbose_name='Provincia')),
                ('postalcode', models.CharField(blank=True, max_length=10, null=True, verbose_name='C\xf3digo Postal')),
                ('iban_code', models.CharField(blank=True, max_length=50, null=True, verbose_name='Cuenta bancaria (IBAN)')),
                ('registration_date', models.DateField(verbose_name='Fecha de alta')),
                ('cr_member', models.BooleanField(default=False, verbose_name='Miembro Consejo Rector')),
            ],
            options={
                'verbose_name': 'Socia',
                'manager_inheritance_from_future': True,
                'verbose_name_plural': 'Socias',
                'permissions': (('mespermission_can_view_accounts', 'Puede ver la lista de socias'),),
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=250, null=True, verbose_name='Nombre')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Descripci\xf3n')),
                ('color', models.CharField(blank=True, max_length=30, null=True, verbose_name='Color de etiqueta (c\xf3digo hexadecimal)')),
            ],
            options={
                'ordering': ['name'],
                'verbose_name': 'Categor\xeda',
                'verbose_name_plural': 'Categor\xedas',
            },
        ),
        migrations.CreateModel(
            name='LegalForm',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250, verbose_name='Nombre')),
            ],
            options={
                'verbose_name': 'Forma legal',
                'verbose_name_plural': 'Formas legales',
            },
        ),
        migrations.CreateModel(
            name='Consumer',
            fields=[
                ('account_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='accounts.Account')),
                ('first_name', models.CharField(blank=True, max_length=250, null=True, verbose_name='Nombre')),
                ('last_name', models.CharField(blank=True, max_length=250, null=True, verbose_name='Apellidos')),
            ],
            options={
                'manager_inheritance_from_future': True,
            },
            bases=('accounts.account',),
        ),
        migrations.CreateModel(
            name='Entity',
            fields=[
                ('account_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='accounts.Account')),
                ('territory', models.CharField(choices=[('local', 'Local'), ('estatal', 'Estatal')], default='local', max_length=20, verbose_name='\xc1mbito')),
                ('assisted_last_fair', models.BooleanField(default=False, verbose_name='Asisti\xf3 a la \xfaltima feria')),
                ('latitude', models.FloatField(default=0, verbose_name='Latitud')),
                ('longitude', models.FloatField(default=0, verbose_name='Longitud')),
                ('logo', imagekit.models.fields.ProcessedImageField(blank=True, null=True, upload_to=helpers.filesystem.RandomFileName('entities/'), verbose_name='Logo en alta resoluci\xf3n')),
                ('banner', imagekit.models.fields.ProcessedImageField(blank=True, null=True, upload_to=helpers.filesystem.RandomFileName('entities/'), verbose_name='Banner alta resoluci\xf3n')),
                ('start_year', models.PositiveSmallIntegerField(blank=True, default=datetime.datetime.now, null=True, validators=[django.core.validators.MinValueValidator(1900), django.core.validators.MaxValueValidator(2019)], verbose_name='A\xf1o de inicio del proyecto')),
                ('contact_person', models.TextField(blank=True, null=True, verbose_name='Persona de contacto')),
            ],
            options={
                'manager_inheritance_from_future': True,
            },
            bases=('accounts.account',),
        ),
        migrations.AddField(
            model_name='account',
            name='legal_form',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.LegalForm', verbose_name='Forma legal'),
        ),
        migrations.AddField(
            model_name='account',
            name='polymorphic_ctype',
            field=models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='polymorphic_accounts.account_set+', to='contenttypes.ContentType'),
        ),
        migrations.CreateModel(
            name='Colaborator',
            fields=[
                ('entity_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='accounts.Entity')),
                ('collaboration', models.TextField(blank=True, verbose_name='Modo de colaboraci\xf3n')),
            ],
            options={
                'manager_inheritance_from_future': True,
            },
            bases=('accounts.entity',),
        ),
        migrations.CreateModel(
            name='Provider',
            fields=[
                ('entity_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='accounts.Entity')),
                ('is_physical_store', models.BooleanField(default=False, verbose_name='Es tienda f\xedsica')),
                ('num_workers', models.IntegerField(default=1, verbose_name='N\xfamero de trabajadoras')),
                ('aprox_income', models.IntegerField(default=0, verbose_name='Facturaci\xf3n \xfaltimo a\xf1o')),
            ],
            options={
                'manager_inheritance_from_future': True,
            },
            bases=('accounts.entity',),
        ),
        migrations.AddField(
            model_name='entity',
            name='categories',
            field=models.ManyToManyField(blank=True, related_name='entities', to='accounts.Category', verbose_name='Categor\xedas'),
        ),
    ]

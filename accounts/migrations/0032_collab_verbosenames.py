# Generated by Django 2.1.12 on 2020-10-08 13:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0031_collab_related_names'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entitycollaboration',
            name='collaboration',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='entities_collab', to='accounts.Collaboration', verbose_name='Modo de colaboración'),
        ),
        migrations.AlterField(
            model_name='entitycollaboration',
            name='custom_fee',
            field=models.FloatField(blank=True, help_text='Cuota anual. Si se deja este campo vacío, se utilizará la cuota por defecto definida en el modo de colaboración', null=True, verbose_name='Cuota específica'),
        ),
        migrations.AlterField(
            model_name='entitycollaboration',
            name='entity',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='entity_colabs', to='accounts.Entity', verbose_name='Entidad'),
        ),
    ]
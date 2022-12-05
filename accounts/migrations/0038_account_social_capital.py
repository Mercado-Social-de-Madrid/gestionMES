# Generated by Django 2.2.28 on 2022-11-17 09:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0037_provider_custom_fee'),
    ]

    operations = [
        migrations.CreateModel(
            name='SocialCapital',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.FloatField(blank=True, default=0, null=True, verbose_name='Capital social')),
                ('paid', models.BooleanField(default=False, verbose_name='Pagado')),
                ('paid_timestamp', models.DateTimeField(blank=True, null=True, verbose_name='Fecha pago')),
                ('returned', models.BooleanField(default=False, verbose_name='Devuelto')),
                ('returned_timestamp', models.DateTimeField(blank=True, null=True, verbose_name='Fecha de devolución')),
            ],
            options={
                'verbose_name': 'Capital social',
                'verbose_name_plural': 'Capitales sociales',
            },
        ),
        migrations.AddField(
            model_name='account',
            name='social_capital',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounts.SocialCapital'),
        ),
    ]
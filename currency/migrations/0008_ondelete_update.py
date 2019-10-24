# Generated by Django 2.1.12 on 2019-10-03 12:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('currency', '0007_guestaccount_cyclos_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='guestaccount',
            name='invited_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='invited_guests', to='accounts.Account', verbose_name='Invitada por'),
        ),
        migrations.AlterField(
            model_name='guestaccount',
            name='token_used',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='invited_guests', to='currency.GuestInvitation', verbose_name='Token utilizado'),
        ),
    ]
# Generated by Django 4.0 on 2022-01-14 09:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='invoice',
            options={'permissions': [('can_change_status', 'Can change status')], 'verbose_name': 'invoice', 'verbose_name_plural': 'invoices'},
        ),
    ]

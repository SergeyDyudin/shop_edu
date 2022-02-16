# Generated by Django 4.0 on 2022-02-16 13:34

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0002_alter_invoice_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='status',
            field=models.PositiveSmallIntegerField(choices=[(0, 'Оплачен'), (1, 'Ожидает оплаты'), (2, 'Отменен')], default=1, verbose_name='status'),
        ),
        migrations.AlterField(
            model_name='rent',
            name='date_to',
            field=models.DateField(default=django.utils.timezone.now, verbose_name='Date to'),
        ),
    ]

# Generated by Django 4.0 on 2022-01-11 15:17

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('books', '0001_initial'),
        ('accounts', '0002_auto_20220110_1002'),
    ]

    operations = [
        migrations.CreateModel(
            name='Invoices',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='date created')),
                ('status_updated', models.DateTimeField(default=django.utils.timezone.now, verbose_name='status updated')),
            ],
            options={
                'verbose_name': 'invoice',
                'verbose_name_plural': 'invoices',
            },
        ),
        migrations.CreateModel(
            name='Statuses',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(max_length=50, unique=True, verbose_name='status')),
            ],
            options={
                'verbose_name': 'status',
                'verbose_name_plural': 'statuses',
            },
        ),
        migrations.CreateModel(
            name='Rents',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveSmallIntegerField(default=1, verbose_name='quantity')),
                ('date_from', models.DateField(default=django.utils.timezone.now, verbose_name='Date from')),
                ('date_to', models.DateField(verbose_name='Date to')),
                ('percentage_per_day', models.FloatField(default=0.1, verbose_name='percentage per day')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='books.items', verbose_name='item')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='services.invoices', verbose_name='order')),
            ],
            options={
                'verbose_name': 'rent',
                'verbose_name_plural': 'rents',
            },
        ),
        migrations.CreateModel(
            name='Purchases',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveSmallIntegerField(default=1, verbose_name='quantity')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='books.items', verbose_name='item')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='services.invoices', verbose_name='order')),
            ],
            options={
                'verbose_name': 'purchase',
                'verbose_name_plural': 'purchases',
            },
        ),
        migrations.AddField(
            model_name='invoices',
            name='status',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='services.statuses', verbose_name='status'),
        ),
        migrations.AddField(
            model_name='invoices',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.customuser', verbose_name='user'),
        ),
    ]

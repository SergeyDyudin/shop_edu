# Generated by Django 4.0 on 2022-01-13 06:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0005_alter_brands_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='items',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='items/photo/', verbose_name='photo'),
        ),
    ]

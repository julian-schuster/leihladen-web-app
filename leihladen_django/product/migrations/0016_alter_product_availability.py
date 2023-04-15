# Generated by Django 4.2 on 2023-04-14 23:59

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0015_product_availability'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='availability',
            field=models.IntegerField(default=1, validators=[django.core.validators.MinValueValidator(0)]),
        ),
    ]

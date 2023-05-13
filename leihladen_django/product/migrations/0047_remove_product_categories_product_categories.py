# Generated by Django 4.2 on 2023-05-10 06:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0046_alter_product_deposit_alter_product_fee'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='categories',
        ),
        migrations.AddField(
            model_name='product',
            name='categories',
            field=models.JSONField(blank=True, default=list),
        ),
    ]
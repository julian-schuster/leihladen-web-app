# Generated by Django 4.2 on 2023-04-07 03:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0008_alter_wishlist_qr_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wishlist',
            name='qr_code',
            field=models.TextField(blank=True, null=True),
        ),
    ]

# Generated by Django 4.2 on 2023-04-07 02:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0004_alter_wishlist_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='wishlist',
            options={'ordering': ['date_added', 0]},
        ),
    ]

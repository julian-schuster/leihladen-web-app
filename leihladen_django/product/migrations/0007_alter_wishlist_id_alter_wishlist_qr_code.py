# Generated by Django 4.2 on 2023-04-07 02:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0006_alter_wishlist_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wishlist',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='wishlist',
            name='qr_code',
            field=models.ImageField(upload_to='qr_codes/'),
        ),
    ]

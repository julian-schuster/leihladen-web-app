# Generated by Django 4.2 on 2023-04-29 01:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0027_rename_image_product_image1_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='image1',
            new_name='image',
        ),
        migrations.RenameField(
            model_name='product',
            old_name='thumbnail1',
            new_name='thumbnail',
        ),
    ]
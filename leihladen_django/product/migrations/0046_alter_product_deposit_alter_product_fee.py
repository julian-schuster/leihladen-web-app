# Generated by Django 4.2 on 2023-05-10 06:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0045_alter_product_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='deposit',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='fee',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]

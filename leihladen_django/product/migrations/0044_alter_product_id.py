# Generated by Django 4.2 on 2023-05-10 05:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0043_remove_product_inventarnummer_alter_product_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='id',
            field=models.CharField(max_length=10, primary_key=True, serialize=False),
        ),
    ]
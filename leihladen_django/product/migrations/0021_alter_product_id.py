# Generated by Django 4.2 on 2023-04-22 00:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0020_delete_admin'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]

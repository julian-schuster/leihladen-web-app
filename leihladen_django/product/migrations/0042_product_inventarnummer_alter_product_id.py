# Generated by Django 4.2 on 2023-05-10 04:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0041_remove_product_category_product_categories'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='inventarnummer',
            field=models.CharField(blank=True, max_length=10, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]

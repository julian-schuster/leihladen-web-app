# Generated by Django 4.2 on 2023-04-22 03:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0022_rename_count_product_quantity_alter_product_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='products/')),
                ('thumbnail', models.ImageField(blank=True, null=True, upload_to='products/')),
            ],
        ),
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ('-date_added',)},
        ),
        migrations.RemoveField(
            model_name='product',
            name='image',
        ),
        migrations.AddField(
            model_name='product',
            name='images',
            field=models.ManyToManyField(to='product.productimage'),
        ),
    ]

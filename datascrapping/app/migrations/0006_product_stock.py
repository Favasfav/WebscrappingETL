# Generated by Django 5.0.6 on 2024-05-26 06:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_remove_product_stock_product_price_unit_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='stock',
            field=models.BooleanField(blank=True, null=True),
        ),
    ]

# Generated by Django 5.0.6 on 2024-05-25 05:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_alter_product_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='quantity',
            field=models.FloatField(blank=True, null=True),
        ),
    ]

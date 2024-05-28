
from django.db import models

class Product(models.Model):
    UNIT_CHOICES = [
        ('ea', 'Each'),
        ('lb', 'Pound'),
        ('ct', 'Count'),
    ]

    name = models.CharField(max_length=255)
    price = models.FloatField(blank=True, null=True)
    price_unit = models.CharField(max_length=10, choices=UNIT_CHOICES, blank=True, null=True)
    quantity = models.FloatField(blank=True, null=True)
    quantity_unit = models.CharField(max_length=10, choices=UNIT_CHOICES, blank=True, null=True)
    product_url = models.URLField(max_length=1000, blank=True, null=True)
    image_url = models.URLField(max_length=500, blank=True, null=True)
    stock = models.BooleanField(blank=True, null=True)
    def __str__(self):
        return self.name


   
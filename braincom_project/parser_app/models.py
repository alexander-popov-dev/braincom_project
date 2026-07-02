from django.db import models

class Product(models.Model):
    title = models.CharField(max_length=500, null=True, blank=True)
    color = models.CharField(max_length=100, null=True, blank=True)
    memory = models.CharField(max_length=100, null=True, blank=True)
    vendor = models.CharField(max_length=200, null=True, blank=True)
    price = models.CharField(max_length=100, null=True, blank=True)
    promo_price = models.CharField(max_length=100, null=True, blank=True)
    photos = models.JSONField(null=True, blank=True)
    product_code = models.CharField(max_length=100, null=True, blank=True)
    reviews_count = models.CharField(max_length=50, null=True, blank=True)
    diagonal = models.CharField(max_length=100, null=True, blank=True)
    display_resolution = models.CharField(max_length=100, null=True, blank=True)
    specifications = models.JSONField(null=True, blank=True)

import datetime
from datetime import timezone

from django.db import models
from auth_.models import Customer, Seller
# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"Category:{self.name}"

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class Product(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='cat_products')
    description = models.CharField(max_length=200)
    price = models.IntegerField(default=0, blank=False)
    amount = models.IntegerField(default=-1)
    location = models.CharField(max_length=100)
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, related_name='sel_products')

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'


class Order(models.Model):
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, related_name='seller_order')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='customer_order')
    total = models.PositiveIntegerField(blank=False)
    products = models.ManyToManyField(Product, related_name='products', blank=True)
    date_created = models.DateTimeField(blank=True, default=datetime.datetime.now())

    def __str__(self):
        return f"Order: {self.pk}"

    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'

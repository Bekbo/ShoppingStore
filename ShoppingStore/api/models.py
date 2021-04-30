import datetime
from datetime import timezone
from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from .addresses import BASE_ADDRESSES
from auth_.models import User, Seller
# Create your models here.


class BaseAddress(models.Model):
    region = models.PositiveSmallIntegerField(choices=BASE_ADDRESSES, unique=True)

    def __str__(self):
        return f"{self.region}"


class ShippingAddress(BaseAddress):
    address = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'ShippingAddress'
        verbose_name_plural = 'ShippingAddresses'

    def __str__(self):
        return f"{self.region}:{self.address}"


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"Category:{self.name}"

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ['name']


class ProductManager(models.Manager):

    def actual(self):
        return self.get_queryset().filter(is_active=True, seller__is_active=True)

    def sort_by_category(self):
        return self.get_queryset().order_by('category')


class Product(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='cat_products')
    description = models.CharField(max_length=200)
    price = models.IntegerField(default=0, blank=False)
    amount = models.IntegerField(default=-1)
    location = models.PositiveSmallIntegerField(choices=BASE_ADDRESSES)
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, related_name='sel_products', default=3)
    is_active = models.BooleanField(default=True)

    objects = ProductManager()

    def __str__(self):
        return f"Product: {self.name}"

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        ordering = ['name']


class OrdersManager(models.Manager):
    def create(self, seller, customer, total=0, del_address=None, *args, **kwargs):
        if seller and customer and del_address:
            order = self.model(seller=seller, customer=customer, total=total, shipping_address=del_address)
            return order
        else:
            raise ValueError('Some fields are not full')

    def add_product(self, product):
        if product:
            order = self.model
            order.products.add(product)
            order.save()
            return order
        else:
            raise ValueError('Some fields are not full')


class Order(models.Model):
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, related_name='seller_order')
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='customer_order')
    total = models.PositiveIntegerField(blank=False)
    products = models.ManyToManyField(Product, related_name='order_products', blank=True)
    date_created = models.DateTimeField(blank=True, default=datetime.datetime.now())
    shipping_address = models.ForeignKey(ShippingAddress, on_delete=models.CASCADE, related_name='order_address')

    orders = OrdersManager()

    def __str__(self):
        return f"Order: {self.pk}"

    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'
        ordering = ['date_created']


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments')
    title = models.CharField(max_length=100)
    body = models.TextField()
    published = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Comment: {self.title}"

    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'
        ordering = ['published']

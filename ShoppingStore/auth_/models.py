from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class User(AbstractUser):
    _gender_choice = (
        (1, 'male'),
        (2, 'female'),
        (0, 'none')
    )
    age = models.IntegerField(default=0, blank=True)
    gender = models.PositiveSmallIntegerField(choices=_gender_choice, default=0)

    def __str__(self):
        return f"User:{self.username}"


class Seller(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='seller')
    shopName = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    shopEmail = models.CharField(max_length=100)
    is_seller = models.BooleanField(default=True)

    def __str__(self):
        return f"Seller:{self.shopName}"

    class Meta:
        verbose_name = 'Seller'
        verbose_name_plural = 'Sellers'


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='customer')
    cardDetails = models.CharField(max_length=100)
    location = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Customer'
        verbose_name_plural = 'Customers'

    def __str__(self):
        return f"Customer:{self.user}"


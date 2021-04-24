from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.contrib.auth.models import AbstractUser
from api.addresses import BASE_ADDRESSES
# Create your models here.


class UserManager(BaseUserManager):
    use_in_migrations = True

    def sellers(self):
        return super().get_queryset().filter(is_seller=True)

    def customers(self):
        return super().get_queryset().filter(is_seller=False)

    def _create_user(self, username, email, password, location, is_seller, **extra_fields):
        if not username:
            raise ValueError('The given username must be set')
        email = self.normalize_email(email)
        username = self.model.normalize_username(username)
        user = self.model(username=username, email=email, location=location, is_seller=is_seller, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        Profile.objects.create(user=user)
        return user

    def create_user(self, username, email=None, password=None, location=-1, is_seller=False,
                    shopName="", shopEmail="",
                    **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        if is_seller:
            user = self._create_user(username, email, password, location, is_seller=True, **extra_fields)
            seller = Seller.objects.create(user=user, shopName=shopName, location=location,
                                           shopEmail=shopEmail)
            return seller
        return self._create_user(username, email, password, location,is_seller=False, **extra_fields)

    def move_to_sellers(self, user, shopName="", shopEmail="", **extra_fields):
        shopEmail = self.normalize_email(shopEmail)
        seller = Seller.objects.create(user=user, shopName=shopName, location=user.location,
                                       shopEmail=shopEmail)
        return seller
#User.objects.create_user(username='bek', email='bek@gmail.com',password='some',location=11, is_seller=True, shopName="someshop", shopEmail="some@gmail.com")


class User(AbstractUser):
    _gender_choice = (
        (1, 'male'),
        (2, 'female'),
        (0, 'none')
    )
    age = models.IntegerField(default=0, blank=True)
    gender = models.PositiveSmallIntegerField(choices=_gender_choice, default=0)
    cardDetails = models.CharField(max_length=100, blank=True, default="")
    location = models.PositiveSmallIntegerField(choices=BASE_ADDRESSES, blank=True, null=True)
    is_seller = models.BooleanField(default=False)

    users = UserManager()

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['username',]

    def __str__(self):
        return f"User : {self.username}"


class Seller(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='seller')
    shopName = models.CharField(max_length=100, blank=False)
    location = models.PositiveSmallIntegerField(choices=BASE_ADDRESSES)
    shopEmail = models.CharField(max_length=100, blank=False)

    def __str__(self):
        return f"Seller : {self.shopName}"

    class Meta:
        verbose_name = 'Seller'
        verbose_name_plural = 'Sellers'
        ordering = ['shopName']


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    products = models.ManyToManyField("api.Product", null=True, blank=True)

    def __str__(self):
        return f"Profile: {self.user.username}"

    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'

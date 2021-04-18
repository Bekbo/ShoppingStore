from django.contrib import admin
from .models import Seller, Customer, User
from api.models import Order, Product, Category
# Register your models here.
admin.site.register(Seller)
admin.site.register(Customer)
admin.site.register(User)
admin.site.register(Order)
admin.site.register(Product)
admin.site.register(Category)
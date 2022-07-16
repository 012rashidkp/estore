from .models import *
from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin

from django.contrib.auth import get_user_model
admin.site.register(get_user_model())


admin.site.register(
    [Admin,Category,Banner, Product, Cart, CartProduct, Order, ProductImage,ProductColor,ProductSize])

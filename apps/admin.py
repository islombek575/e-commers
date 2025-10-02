from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from apps.models import UserProfile, Product


# TODO adminkada project nomini adminkaga chiqarib qoyish kk

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('email', 'phone', 'password')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'price', ]

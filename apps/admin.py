from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from apps.models import Category, ProductImage, Like
from .models import Product
from .models import User
from .models.products import Comment, ProductVersion


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


class ProductVersionInline(admin.TabularInline):
    model = ProductVersion
    extra = 1
    # form = ProductVersionForm


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'created_at')
    search_fields = ('name',)
    list_filter = ('category',)
    inlines = [ProductImageInline, ProductVersionInline]


@admin.register(User)
class UserModelAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('phone', 'password')}),
        ('Personal info', {'fields': ('email', 'address',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone', 'email', 'address', 'password1', 'password2', 'is_staff', 'is_superuser'),
        }),
    )

    list_display = ('phone', 'email', 'is_staff', 'is_superuser')
    search_fields = ('phone', 'email')
    ordering = ('-id',)


admin.site.register(Category)
admin.site.register(Like)
admin.site.register(Comment)

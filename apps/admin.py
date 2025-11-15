from apps.models import Cart, CartItem, Like, Order, ProductImage
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Category, Product, User
from .models.products import Comment, ProductVersion
from .models.users import Merchant, Shop


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


class ProductVersionInline(admin.TabularInline):
    model = ProductVersion
    min_num = 1
    extra = 0


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
        ('Personal info', {'fields': ('email', 'address', 'role')}),
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


@admin.register(Order)
class OrderModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'total_amount', 'status', 'created_at']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'parent')
    list_display_links = ('id',)
    search_fields = ('name',)


admin.site.register(Shop)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Like)
admin.site.register(Comment)
admin.site.register(Merchant)

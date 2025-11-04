from django.contrib import admin
from django_json_widget.widgets import JSONEditorWidget
from rest_framework.fields import JSONField

from apps.models import Category, ProductImage, Like
from .forms import ProductVersionForm
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
class UserAdmin(admin.ModelAdmin):
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

    def save_model(self, request, obj, form, change):
        raw_pwd = form.cleaned_data.get('password')
        if raw_pwd and not raw_pwd.startswith('argon2$'):
            obj.set_password(raw_pwd)
        super().save_model(request, obj, form, change)


admin.site.register(Category)
admin.site.register(Like)
admin.site.register(Comment)

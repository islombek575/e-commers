from django.contrib import admin
from django.db.models import JSONField
from django_json_widget.widgets import JSONEditorWidget

from apps.models import Category, ProductImage, Like
from .forms import ProductForm
from .models import Product
from .models.products import Comment


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'discount', 'created_at')
    search_fields = ('name',)
    list_filter = ('category',)
    inlines = [ProductImageInline]
    formfield_overrides = {
        JSONField: {'widget': JSONEditorWidget},
    }
    form = ProductForm


from django.contrib import admin
from .models import User


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

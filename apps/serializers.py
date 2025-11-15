import re
from typing import Any

from django.contrib.auth import authenticate
from drf_spectacular.utils import extend_schema_field
from rest_framework.exceptions import ValidationError
from rest_framework.fields import (
    CharField,
    DictField,
    IntegerField,
    ListField,
    SerializerMethodField,
)
from rest_framework.serializers import ModelSerializer, Serializer
from rest_framework_simplejwt.tokens import RefreshToken, Token

from .models import Cart, CartItem, Category, Like, Order, OrderItem, Product, ProductImage, User
from .models.products import Comment, ProductVersion
from .models.users import Shop


class SendSmsCodeSerializer(Serializer):
    phone = CharField(default='901001010')

    def validate_phone(self, value):
        digits = re.findall(r'\d', value)
        if len(digits) < 9:
            raise ValidationError('Phone number must be at least 9 digits')

        phone = ''.join(digits)
        return phone.removeprefix('998')

    def validate(self, attrs):
        phone = attrs['phone']
        user, created = User.objects.get_or_create(phone=phone)
        user.set_unusable_password()

        return super().validate(attrs)


class VerifySmsCodeSerializer(Serializer):
    phone = CharField(default='901001010')
    code = IntegerField(default=100100)
    token_class = RefreshToken

    def validate_phone(self, value):
        digits = re.findall(r'\d', value)
        if len(digits) < 9:
            raise ValidationError('Phone number must be at least 9 digits')
        phone = ''.join(digits)
        return phone.removeprefix('998')

    def validate(self, attrs: dict[str, Any]):
        phone_number = attrs['phone']

        try:
            user_obj = User.objects.get(phone=phone_number)

            authenticated_user = authenticate(phone=phone_number, request=self.context['request'])
            if authenticated_user is not None:
                self.user = authenticated_user
            else:
                if not user_obj.is_active:
                    raise ValidationError("Foydalanuvchi faol emas. Ma'muriyatga murojaat qiling.")
                self.user = user_obj

        except User.DoesNotExist:
            try:
                self.user = User.objects.create(phone=phone_number)
            except Exception as e:
                print(f"User yaratishda xato: {e}")
                raise ValidationError(
                    "Foydalanuvchini yaratishda kutilmagan xato yuz berdi. Iltimos, keyinroq urinib ko'ring.")

        if self.user is None or not self.user.is_active:
            raise ValidationError("Foydalanuvchini topish, yaratish yoki faollikni tekshirishda xato yuz berdi.")

        return attrs

    @property
    def get_data(self):
        refresh = self.get_token(self.user)
        data = {
            'access_token': str(refresh.access_token),
            'refresh_token': str(refresh)
        }
        user_data = UserModelSerializer(self.user).data

        return {
            'message': 'OK.',
            'data': {
                **data, **{'user': user_data}
            }
        }

    @classmethod
    def get_token(cls, user) -> Token:
        return cls.token_class.for_user(user)


class UserModelSerializer(ModelSerializer):
    password = CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'phone', 'address', 'password']


class CommentModelSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'user', 'rate']


class ProductImageModelSerializer(ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image']


class ProductVersionModelSerializer(ModelSerializer):
    class Meta:
        model = ProductVersion
        fields = '__all__'


class ProductListModelSerializer(ModelSerializer):
    images = ProductImageModelSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'category', 'slug', 'name', 'images', 'price']


class ProductDetailModelSerializer(ModelSerializer):
    images = ProductImageModelSerializer(many=True, read_only=True)
    product_versions = ProductVersionModelSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = '__all__'


class CategoryModelSerializer(ModelSerializer):
    sub_categories = SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'slug', 'icon', 'sub_categories']

    @extend_schema_field(ListField(child=DictField()))
    def get_sub_categories(self, obj):
        sub_cats = obj.sub_categories.all()
        serializer = CategoryModelSerializer(sub_cats, many=True, context=self.context)
        return serializer.data


class LikeSerializer(ModelSerializer):
    class Meta:
        model = Like
        fields = ['id', 'user', 'product']


class CartModelSerializer(ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'


class CartItemModelSerializer(ModelSerializer):
    class Meta:
        model = CartItem
        fields = 'id', 'cart', 'product_version', 'quantity'
        read_only_fields = 'cart', 'quantity'

    def create(self, validated_data):
        user = self.context['request'].user
        cart = Cart.objects.filter(user=user).first()
        if not cart:
            cart = Cart.objects.create(user=user)

        return super().create(validated_data | {'cart_id': cart.id})


class OrderModelSerializer(ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'


class OrderItemModelSerializer(ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'


class ShopModelSerializer(ModelSerializer):
    products = ProductListModelSerializer(many=True, read_only=True)

    class Meta:
        model = Shop
        fields = '__all__'

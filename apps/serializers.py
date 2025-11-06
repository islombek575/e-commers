import re
from typing import Any

from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.fields import CharField
from rest_framework.serializers import Serializer
from rest_framework_simplejwt.tokens import RefreshToken, Token

from .models import Category, Like, Product, ProductImage, User
from .models.products import Comment


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


class VerifySmsCodeSerializer(serializers.Serializer):
    phone = serializers.CharField(default='901001010')
    code = serializers.IntegerField(default=100100)
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


class UserModelSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'phone', 'address', 'password']


class CommentModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'user', 'rate']


class ProductImageModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image']


class ProductModelSerializer(serializers.ModelSerializer):
    images = ProductImageModelSerializer(many=True, read_only=True)
    final_price = serializers.ReadOnlyField()

    class Meta:
        model = Product
        fields = ['id', 'name', 'images', 'final_price']


class CategoryModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'icon']


class LikeSerializer(serializers.ModelSerializer):
    user = UserModelSerializer(read_only=True)
    product = ProductModelSerializer(read_only=True)

    class Meta:
        model = Like
        fields = ['id', 'user', 'product']

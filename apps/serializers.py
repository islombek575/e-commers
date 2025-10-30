import re
from typing import Any
from django.core.cache import cache
from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.fields import IntegerField, CharField
from rest_framework.serializers import Serializer
from rest_framework_simplejwt.tokens import RefreshToken, Token

from .models import (
    Category, Product,
    ProductImage, Like, User
)
from .models.products import Comment
from .utils import check_sms_code


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
    code = IntegerField()
    token_class = RefreshToken

    def validate(self, attrs):
        request = self.context['request']
        phone = cache.get(f"verify:current_phone:{request.session.session_key}")

        if not phone:
            raise ValidationError({'message': "Telefon raqam topilmadi. Qaytadan urinib ko‘ring"})

        code = attrs.get("code")
        if not check_sms_code(phone, code):
            raise ValidationError({"message": "Kod noto‘g‘ri yoki muddati tugagan"})

        # ✅ Agar user mavjud bo‘lmasa, yangi user yaratamiz
        user, created = User.objects.get_or_create(phone=phone)
        if created:
            user.set_unusable_password()
            user.save()

        attrs["user"] = user
        return attrs

    @property
    def get_data(self):
        user = self.validated_data["user"]
        refresh = self.token_class.for_user(user)
        data = {
            "access_token": str(refresh.access_token),
            "refresh_token": str(refresh),
            "user": UserModelSerializer(user).data
        }
        return {"message": "OK", "data": data}



class UserModelSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'phone', 'address', 'password']


class CommentModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'user', 'comment']


class ProductImageModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image']


class ProductModelSerializer(serializers.ModelSerializer):
    images = ProductImageModelSerializer(many=True, read_only=True)
    final_price = serializers.ReadOnlyField()
    comments = CommentModelSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'images', 'final_price', 'comments']


class CategoryModelSerializer(serializers.ModelSerializer):
    products = ProductModelSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'icon', 'products']


class LikeSerializer(serializers.ModelSerializer):
    user = UserModelSerializer(read_only=True)
    product = ProductModelSerializer(read_only=True)

    class Meta:
        model = Like
        fields = ['id', 'user', 'product']

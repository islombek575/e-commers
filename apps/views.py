from django.core.cache import cache
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Category, Product, Like, User
from .models.products import Comment
from .serializers import CategoryModelSerializer, ProductModelSerializer, LikeSerializer, SendSmsCodeSerializer, \
    VerifySmsCodeSerializer, UserModelSerializer
from .utils import random_code, send_sms_code, check_sms_code


@extend_schema(tags=['Auth'])
class SendCodeAPIView(APIView):
    serializer_class = SendSmsCodeSerializer
    authentication_classes = ()

    def post(self, request, *args, **kwargs):
        serializer = SendSmsCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        code = random_code()
        phone = serializer.data['phone']
        send_sms_code(phone, code)
        cache.set(f"verify:current_phone:{request.session.session_key}", phone, 300)
        return Response({"message": "send sms code"})


@extend_schema(tags=['Auth'])
class LoginAPIView(APIView):
    serializer_class = VerifySmsCodeSerializer
    authentication_classes = ()

    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        session_key = request.session.session_key
        phone = cache.get(f"verify:current_phone:{session_key}")

        if not phone:
            return Response({"message": "Telefon raqam topilmadi, qayta urinib ko‘ring"}, status.HTTP_400_BAD_REQUEST)

        code = serializer.validated_data.get('code')
        if not check_sms_code(phone, code):
            return Response({"message": "Kod noto‘g‘ri yoki muddati tugagan"}, status.HTTP_400_BAD_REQUEST)

        user, created = User.objects.get_or_create(phone=phone)
        if created:
            user.set_unusable_password()
            user.save()

        refresh = RefreshToken.for_user(user)
        data = {
            "access_token": str(refresh.access_token),
            "refresh_token": str(refresh),
            "user": UserModelSerializer(user).data,
        }
        return Response({"message": "OK", "data": data})


class CategoryListView(ListAPIView):
    queryset = Category.objects.all().order_by('name')
    serializer_class = CategoryModelSerializer


class ProductListView(ListCreateAPIView):
    queryset = Product.objects.select_related('category')
    serializer_class = ProductModelSerializer


class ProductDetailView(RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductModelSerializer


class LikeCreateView(CreateAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, product_id=self.kwargs['product_id'])


class CommentCreateView(CreateAPIView):
    queryset = Comment.objects.all().filter()
    serializer_class = CategoryModelSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, product_id=self.kwargs['product_id'])

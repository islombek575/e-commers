from apps.models import Category, Comment, Like, Product
from apps.serializers import (
    CategoryModelSerializer,
    CommentModelSerializer,
    LikeSerializer,
    ProductDetailModelSerializer,
    ProductListModelSerializer,
    SendSmsCodeSerializer,
    VerifySmsCodeSerializer,
)
from apps.utils import check_sms_code, random_code, send_sms_code
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


@extend_schema(tags=['Auth'])
class SendCodeAPIView(APIView):
    serializer_class = SendSmsCodeSerializer
    authentication_classes = ()

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone = serializer.validated_data['phone']

        result = send_sms_code(phone)
        if not result["success"]:
            return Response(
                {"message": f"Please wait {result['remaining']} seconds before requesting a new code."},
                status=429
            )

        return Response({"message": f"SMS code sent. You have {result['remaining']} seconds before requesting again."})


@extend_schema(tags=['Auth'])
class LoginAPIView(APIView):
    serializer_class = VerifySmsCodeSerializer
    authentication_classes = ()

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        is_valid_code = check_sms_code(**serializer.data)
        if not is_valid_code:
            return Response({"message": "invalid code"}, status.HTTP_400_BAD_REQUEST)

        return Response(serializer.get_data)


class CategoryListView(ListAPIView):
    queryset = Category.objects.all().filter(parent__isnull=True)
    serializer_class = CategoryModelSerializer


class ProductListView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductListModelSerializer


class ProductDetailView(RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductDetailModelSerializer


class LikeCreateView(CreateAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, product_id=self.kwargs['product_id'])


class CommentCreateView(CreateAPIView):
    queryset = Comment.objects.all().filter()
    serializer_class = CommentModelSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, product_id=self.kwargs['product_id'])

from apps.filters import ProductPriceFilter
from apps.models import Cart, CartItem, Category, Comment, Like, Product
from apps.models.users import Shop
from apps.paginations import CustomProductPagination
from apps.serializers import (
    CartItemModelSerializer,
    CartModelSerializer,
    CategoryModelSerializer,
    CommentModelSerializer,
    LikeSerializer,
    ProductDetailModelSerializer,
    ProductListModelSerializer,
    SendSmsCodeSerializer,
    ShopModelSerializer,
    VerifySmsCodeSerializer,
)
from apps.utils import check_sms_code, random_code, send_sms_code
from django.db.models import Min
from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.exceptions import NotAuthenticated
from rest_framework.generics import CreateAPIView, ListAPIView, ListCreateAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


@extend_schema(tags=['Auth'])
class SendCodeAPIView(APIView):
    serializer_class = SendSmsCodeSerializer
    authentication_classes = ()

    def post(self, request, *args, **kwargs):
        serializer = SendSmsCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone = request.data.get("phone")
        if not phone:
            return Response({"detail": "Telefon raqami kerak!"}, status=status.HTTP_400_BAD_REQUEST)

        code = random_code()
        valid, _ttl = send_sms_code(phone, code)

        if valid:
            return Response({"detail": _("SMS code sent !")})

        return Response(
            {"detail": _(f"You can send again in {int(_ttl)} seconds.")},
            status=status.HTTP_429_TOO_MANY_REQUESTS
        )


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
    queryset = Category.objects.filter(parent__isnull=True)
    serializer_class = CategoryModelSerializer


class ProductListView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductListModelSerializer
    pagination_class = CustomProductPagination

    filterset_class = ProductPriceFilter

    search_fields = ['name', 'description', 'category__name']

    ordering_fields = ['min_price', 'created_at']

    def get_queryset(self):
        return super().get_queryset().annotate(
            min_price=Min('product_versions__price')
        )


class ProductDetailView(RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductDetailModelSerializer


class LikeCreateView(CreateAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, product_id=self.kwargs['product_id'])


class WishList(ListAPIView):
    serializer_class = LikeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_anonymous:
            raise NotAuthenticated(_("You are not authenticated"))
        return Like.objects.filter(user=user)


class CommentCreateView(CreateAPIView):
    queryset = Comment.objects.all().filter()
    serializer_class = CommentModelSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, product_id=self.kwargs['product_id'])


@extend_schema(tags=['Cart & CartItem'])
class CartListCreateView(ListCreateAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartModelSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_anonymous:
            raise NotAuthenticated(_("You are not authenticated"))
        return Cart.objects.filter(customer=user)


@extend_schema(tags=['Cart & CartItem'])
class CartItemListCreateView(ListCreateAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemModelSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_anonymous:
            raise NotAuthenticated(_("You are not authenticated"))
        return CartItem.objects.filter(cart__customer=user)


class ShopDetailAPIView(RetrieveAPIView):
    queryset = Shop.objects.all()
    serializer_class = ShopModelSerializer

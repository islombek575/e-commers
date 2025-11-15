from apps.views import (
    CartItemListCreateView,
    CartListCreateView,
    CategoryListView,
    LikeCreateView,
    LoginAPIView,
    ProductDetailView,
    ProductListView,
    SendCodeAPIView,
    ShopDetailAPIView,
    WishList,
)
from django.urls import path

urlpatterns = [
    path('auth/send-code/', SendCodeAPIView.as_view(), name='token_obtain_pair'),
    path('auth/verify-code/', LoginAPIView.as_view(), name='token_obtain_pair'),
    path('categories/', CategoryListView.as_view(), name='category_list'),
    path('products/', ProductListView.as_view(), name='product_list'),
    path('wishList/', WishList.as_view(), name='wish_list'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('products/<int:product_id>/like/', LikeCreateView.as_view(), name='like_create'),
    path('cart/', CartListCreateView.as_view(), name='cart_create'),
    path('cartitem/', CartItemListCreateView.as_view(), name='cart_item'),
    path('shop/<int:pk>/', ShopDetailAPIView.as_view(), name='shop_detail'),

]

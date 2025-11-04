from django.urls import path
from .views import (
    CategoryListView, ProductListView, ProductDetailView, LikeCreateView, SendCodeAPIView,
    LoginAPIView, SubCategoryListView
)

urlpatterns = [
    path('auth/send-code', SendCodeAPIView.as_view(), name='token_obtain_pair'),
    path('auth/verify-code', LoginAPIView.as_view(), name='token_obtain_pair'),
    path('categories/', CategoryListView.as_view(), name='category_list'),
    path('subcategories/', SubCategoryListView.as_view(), name='subcategory_list'),
    path('products/', ProductListView.as_view(), name='product_list'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('products/<int:product_id>/like/', LikeCreateView.as_view(), name='like_create'),
]

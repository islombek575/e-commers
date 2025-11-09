import django_filters
from apps.models.products import Product
from django.db.models import Min


class ProductPriceFilter(django_filters.FilterSet):
    price_min = django_filters.NumberFilter(method='filter_by_price_min', label="Minimal narx")
    price_max = django_filters.NumberFilter(method='filter_by_price_max', label="Maksimal narx")

    shop_id = django_filters.NumberFilter(
        field_name='shop__id',
        lookup_expr='exact',
        label="Do'kon IDsi"
    )

    class Meta:
        model = Product
        fields = ['shop_id', 'price_min', 'price_max']

    def filter_by_price_min(self, queryset, name, value):
        return queryset.annotate(
            min_price=Min('product_versions__price')
        ).filter(min_price__gte=value)

    def filter_by_price_max(self, queryset, name, value):
        return queryset.annotate(
            min_price=Min('product_versions__price')
        ).filter(min_price__lte=value)

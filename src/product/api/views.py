from rest_framework import viewsets, filters
from product.api import filters as filters_product
from product.api import pagination as pagination_global
from product.api import serializers as serializers_product
from product import models as models_product


class ProductViewSet(viewsets.ModelViewSet):
    queryset = models_product.Product.objects.all()
    serializer_class = serializers_product.ProductSerializer
    pagination_class = pagination_global.GlobalPagination
    filter_backends = [filters.SearchFilter]
    search_fields = [
        "title",
        "description",
    ]


class VariantViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models_product.Variant.objects.all()
    serializer_class = serializers_product.VariantSerializer
    pagination_class = pagination_global.GlobalPagination
    filter_backends = [filters.SearchFilter]
    search_fields = [
        "title",
        "description",
    ]

from django.urls import path, include
from rest_framework import routers
from product.api import views as views_product

simple_router = routers.SimpleRouter(trailing_slash=True)
simple_router.register(r"products", views_product.ProductViewSet, basename="product")
simple_router.register(r"variants", views_product.VariantViewSet, basename="variant")


urlpatterns = [
    path("", include(simple_router.urls)),
]

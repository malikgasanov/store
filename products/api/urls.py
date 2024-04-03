from django.urls import path, include

urlpatterns = [
    path("v1/products/", include("products.api.v1.urls", namespace="products_v1")),
]

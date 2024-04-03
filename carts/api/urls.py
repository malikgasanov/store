from django.urls import path, include

urlpatterns = [
    path("v1/carts/", include("carts.api.v1.urls", namespace="carts_v1")),
]

from django.urls import path, include
from rest_framework import routers

from products.api.v1.views import ProductViewSet, CategoryViewSet

app_name = "products"

router = routers.SimpleRouter()
router.register(r'', ProductViewSet)
router.register(r'categories', CategoryViewSet)

urlpatterns = [
]

urlpatterns += router.urls

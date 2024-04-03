from django.urls import path
from rest_framework import routers

from carts.api.v1.views import CartViewSet

app_name = "carts"

router = routers.SimpleRouter()
router.register(r'', CartViewSet)

urlpatterns = []

urlpatterns += router.urls

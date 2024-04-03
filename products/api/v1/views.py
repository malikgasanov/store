from drf_spectacular.utils import extend_schema

from products.api.v1.serializers import ProductSerializer, CategorySerializer
from products.models import Product, Category
from store.viewsets import CreateListViewSet, CreateRetrieveListViewSet


@extend_schema(tags=['Product'])
class ProductViewSet(CreateRetrieveListViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


@extend_schema(tags=['Category'])
class CategoryViewSet(CreateListViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer



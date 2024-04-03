from django.db import transaction, IntegrityError
from django.http import JsonResponse
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from carts.api.v1.serializers import CartSerializer
from carts.models import Cart, CartProduct
from orders.models import Order
from payments.tasks import send_payment
from store.viewsets import ListViewSet


@extend_schema(tags=['Cart'])
class CartViewSet(ListViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

    def get_object(self):
        return get_object_or_404(self.queryset, user=self.request.user)

    def __cart_clean(self):
        self.object.cartproduct_set.all().delete()

    def __order_registration(self):
        order = Order.objects.create(user=self.object.user)
        for cart_product in self.object.cartproduct_set.all():
            order.orderposition_set.create(
                product=cart_product.product,
                quantity=cart_product.quantity
            )
        return order

    def __add_cart_product(self, products):
        self.object = self.get_object()
        for product in products:
            obj = CartProduct(
                cart=self.object,
                product_id=product['product'],
                quantity=product['quantity']
            )
            obj.save()

    @action(methods=['post'], detail=False)
    def add(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        products = request.data.pop('products')
        try:
            self.__add_cart_product(products)
        except IntegrityError:
            return Response({'message': 'Данный товар уже в корзине'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(methods=['post'], detail=False)
    def registration(self, request):
        self.object = self.get_object()
        with transaction.atomic():
            order = self.__order_registration()
            if order:
                self.__cart_clean()
        send_payment.delay(order_id=order.pk)
        return JsonResponse({'message': 'Вам на почту отправлено сообщение'})






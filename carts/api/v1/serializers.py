from django.contrib.auth import get_user_model
from django.db import transaction
from rest_framework import serializers

from carts.models import Cart, CartProduct

User = get_user_model()

class CartProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartProduct
        fields = [
            'product',
            'quantity'
        ]


class CartSerializer(serializers.ModelSerializer):
    products = CartProductSerializer(many=True, source='cartproduct_set')

    class Meta:
        model = Cart
        fields = [
            'id',
            'user',
            'products',
        ]
        read_only_fields = ['user']


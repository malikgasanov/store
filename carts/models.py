from django.db import models

from django.contrib.auth import get_user_model
from django.db.models import F, Q, Exists, OuterRef
from rest_framework.exceptions import ValidationError

from products.models import Product

User = get_user_model()


class Cart(models.Model):
    user = models.ForeignKey(User, models.CASCADE, verbose_name='пользователь')

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзина'
        unique_together = ['user']

    def __str__(self):
        return str(self.pk)


class CartProduct(models.Model):
    cart = models.ForeignKey(Cart, models.CASCADE, verbose_name='корзина')
    product = models.ForeignKey(Product, models.CASCADE, verbose_name='продукт')
    quantity = models.PositiveIntegerField('количество', default=1)

    class Meta:
        verbose_name = 'Товар в корзине'
        verbose_name_plural = 'Товары в корзине'
        unique_together = ['cart', 'product']

    def clean(self):
        if self.product.stock_quantity < self.quantity:
            raise ValidationError('Количество товара превышает допустимое значение')

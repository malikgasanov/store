from django.db import models

from django.contrib.auth import get_user_model

from orders.querysets import OrderQuerySet
from products.models import Product

User = get_user_model()


class Order(models.Model):
    class Status(models.TextChoices):
        CREATED = 'CREATED', 'Создан'
        CANCELED = 'CANCELED', 'Отменен'
        ACCEPTED = 'ACCEPTED', 'Принято'
        COMPLETED = 'COMPLETED', 'Завершен'
        REFUND = 'REFUND', 'Возврат денег'
        PENDING = 'PENDING', 'Ожидает оплаты'
        SUCCEEDED = "SUCCEEDED", "Оплачен"

    user = models.ForeignKey(User, models.CASCADE, verbose_name="пользователь")
    created_at = models.DateTimeField("дата создания", auto_now_add=True)
    status = models.CharField('статус', choices=Status.choices, default=Status.CREATED)
    reason_cancellation = models.TextField("причина отмены", null=True, blank=True)
    objects = OrderQuerySet.as_manager()

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'


class OrderPosition(models.Model):
    order = models.ForeignKey(Order, models.CASCADE)
    product = models.ForeignKey(Product, models.PROTECT)
    quantity = models.PositiveIntegerField('количество', default=1)

    class Meta:
        verbose_name = 'Позиция заказа'
        verbose_name_plural = 'Позиции заказа'



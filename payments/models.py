from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

User = get_user_model()


class Payment(models.Model):
    class Status(models.TextChoices):
        AUTHORIZED = "AUTHORIZED", "Ожидает подтверждения"
        COMPLETED = "COMPLETED", "Оплачен"
        CANCELED = "CANCELLED", "Отменен"
        DECLINED = "DECLINED", "Отклонен"
        REFUND = 'REFUND', 'Возврат денег'

    user = models.ForeignKey(User, models.CASCADE, verbose_name="пользователь", related_name="payments")
    transaction_id = models.BigIntegerField("id транзакции", unique=True)
    invoice_id = models.CharField("номер операции", null=True, blank=True)
    error_code = models.PositiveIntegerField("код ошибки", null=True, blank=True)
    error_message = models.TextField("сообщение об ошибке", null=True, blank=True)
    status = models.CharField("статус", choices=Status.choices, default=Status.AUTHORIZED, db_index=True)
    amount = models.DecimalField("сумма", max_digits=10, decimal_places=2, default=0.00)
    details = models.JSONField("детали платежа", blank=True, null=True)
    created = models.DateTimeField("дата создания", auto_now_add=True, db_index=True)
    updated = models.DateTimeField("дата изменения", auto_now=True, db_index=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()

    class Meta:
        verbose_name = 'Платеж'
        verbose_name_plural = 'Платежи'

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models


User = get_user_model()


class Notification(models.Model):
    class Status(models.TextChoices):
        CREATED = 'CREATED', 'Создан'
        SUCCEEDED = 'SUCCEEDED', 'Успешно'
        ERROR = 'ERROR', 'Ошибка'

    status = models.CharField('статус', max_length=50, choices=Status.choices, default=Status.CREATED)
    recipient = models.ForeignKey(User, models.CASCADE, verbose_name='получатель', blank=False)
    verb = models.CharField('заголовок', max_length=255)
    description = models.TextField('описание', blank=True, null=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()
    data = models.JSONField('детали', blank=True, null=True)

    class Meta:
        verbose_name = 'Уведомление'
        verbose_name_plural = 'Уведомления'


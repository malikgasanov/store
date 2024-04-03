import json

import requests
from celery import shared_task
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from requests import RequestException

from notifications.models import Notification
from orders.models import Order

User = get_user_model()


@shared_task(
    bind=True,
    autoretry_for=(RequestException,),
    max_retries=5,
    retry_backoff=True,
)
def send_payment(self, order_id):
    order = Order.objects.get(pk=order_id)
    data = Order.objects.filter(pk=order.pk).with_amount_and_count()
    data['amount'] = data['discount_price'] or data['price']
    response = requests.post(
        url=settings.PAYMENT_MEDIANN_URL,
        data=json.dumps({
            'api_token': settings.PAYMENT_MEDIANN_TOKEN,
            'user_email': order.user.email,
            'amount': data['amount'],
            'items_qty': data['count']
        })
    )
    response.raise_for_status()
    if response.status_code == 200:
        Notification.objects.create(
            verb='Потдверждение оплаты',
            data=json.loads(response.content.decode('utf-8')),
            recipient=order.user,
            content_type=ContentType.objects.get_for_model(order.__class__),
            object_id=order.pk
        )




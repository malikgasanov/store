import smtplib

from celery import shared_task
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.template.loader import render_to_string

from notifications.models import Notification

User = get_user_model()


@shared_task(
    bind=True,
    autoretry_for=(smtplib.SMTPException,),
    max_retries=10,
    retry_backoff=True)
def send_payment_confirmation_email(self):
    for notification in Notification.objects.filter(status=Notification.Status.CREATED):
        message = render_to_string(
            'email/payment_confirmation_email.html',
            notification.data
        )
        response = send_mail(
            notification.verb,
            message,
            settings.EMAIL_HOST_USER,
            [notification.recipient.email]
        )
        if response:
            notification.status = Notification.Status.SUCCEEDED
            notification.save()

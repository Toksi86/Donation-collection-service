from __future__ import absolute_import, unicode_literals
from celery import shared_task
from django.core.mail import EmailMessage

@shared_task
def send_confirmation_email_task(user_email):
    email = EmailMessage(
        'Вы успешно создали пожертвование.',
        'Успешное пожертвование',
        'dcs@example.com',
        [user_email],
    )
    email.send()
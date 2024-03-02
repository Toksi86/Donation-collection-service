from __future__ import absolute_import, unicode_literals

from celery import shared_task
from django.core.mail import EmailMessage


@shared_task
def send_payment_confirmation_email_task(request):
    email = EmailMessage(
        'Вы отправили пожертвование',
        f'Вы отправили пожертвование на сумму {request.data['amount']}',
        'dcs@example.com',
        [request.user.email],
    )
    email.send()


@shared_task
def send_payment_received_email_task(request, collect_instance):
    email = EmailMessage(
        f'По вашему сбору {collect_instance.title} поступило пожертвование',
        f'По вашему сбору {collect_instance.title} поступило пожертвование на сумму {request.data['amount']}.',
        'dcs@example.com',
        [collect_instance.author.email],
    )
    email.send()


@shared_task
def send_collect_confirmation_email_task(request):
    email = EmailMessage(
        'Успешное создание сбора',
        f'Вы успешно создали сбор с заголовком {request.data['title']}.',
        'dcs@example.com',
        [request.user.email],
    )
    email.send()

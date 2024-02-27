from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from donation_app.models import Reason, Collect, Payment
from faker import Faker

User = get_user_model()
fake = Faker()


class Command(BaseCommand):
    help = 'Наполняет базу данных моковыми данными'

    def handle(self, *args, **options):
        self.stdout.write('Запущена программа наполнения базы данных...')

        for _ in range(10):
            User.objects.create_user(
                username=fake.user_name(),
                email=fake.email(),
                password=fake.password()
            )

        for _ in range(10):
            Reason.objects.create(title=fake.sentence())

        for _ in range(100):
            Collect.objects.create(
                author=User.objects.order_by('?').first(),
                title=fake.sentence(),
                reason=Reason.objects.order_by('?').first(),
                description=fake.text(),
                planned_amount=fake.pydecimal(left_digits=2, right_digits=2, positive=True),
                end_date=fake.date_between(start_date='today', end_date='+1y')
            )

        for _ in range(1000):
            Payment.objects.create(
                user=User.objects.order_by('?').first(),
                title=fake.sentence(),
                description=fake.text(),
                amount=fake.pydecimal(left_digits=2, right_digits=2, positive=True),
                collect=Collect.objects.order_by('?').first()
            )

        self.stdout.write(self.style.SUCCESS('База данных наполнена моковыми данными.'))

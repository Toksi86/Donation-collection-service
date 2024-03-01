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

        users = [User(
            username=fake.user_name(),
            email=fake.email(),
            password=fake.password()
        ) for _ in range(10)]
        User.objects.bulk_create(users)

        reasons = [Reason(title=fake.sentence()) for _ in range(10)]
        Reason.objects.bulk_create(reasons)

        collects = [Collect(
            author=User.objects.order_by('?').first(),
            title=fake.sentence(),
            reason=Reason.objects.order_by('?').first(),
            description=fake.text(),
            planned_amount=fake.pydecimal(left_digits=2, right_digits=2, positive=True),
            end_date=fake.date_between(start_date='today', end_date='+1y')
        ) for _ in range(100)]
        Collect.objects.bulk_create(collects)

        payments = [Payment(user=User.objects.order_by('?').first(), title=fake.sentence(), description=fake.text(),
                            amount=fake.pydecimal(left_digits=2, right_digits=2, positive=True),
                            collect=Collect.objects.order_by('?').first()) for _ in range(1000)]
        Payment.objects.bulk_create(payments)

        self.stdout.write(self.style.SUCCESS('База данных наполнена моковыми данными.'))

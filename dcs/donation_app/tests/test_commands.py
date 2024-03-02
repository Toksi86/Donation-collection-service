from django.core.management import call_command
from django.test import TestCase
from donation_app.models import User, Reason, Collect, Payment


class PopulateDatabaseTest(TestCase):
    def test_populate_database(self):
        # Вызов команды для наполнения базы данных
        call_command('populate_db')

        # Проверка, что данные были добавлены
        self.assertEqual(User.objects.count(), 10)
        self.assertEqual(Reason.objects.count(), 10)
        self.assertEqual(Collect.objects.count(), 100)
        self.assertEqual(Payment.objects.count(), 1000)

        # Проверка, что данные в базе данных соответствуют ожидаемым
        self.assertIsNotNone(User.objects.first().username)
        self.assertIsNotNone(Reason.objects.first().title)
        self.assertIsNotNone(Collect.objects.first().title)
        self.assertIsNotNone(Payment.objects.first().title)

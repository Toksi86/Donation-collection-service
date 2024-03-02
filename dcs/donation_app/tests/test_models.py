from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.test import TestCase
from donation_app.models import Reason, Collect, Payment
from donation_app.serializers import PaymentSerializer

User = get_user_model()


class ReasonModelTest(TestCase):
    def setUp(self):
        self.reason = Reason.objects.create(title="Test Reason")

    def test_create_reason(self):
        self.assertEqual(self.reason.title, "Test Reason")

    def test_str_method(self):
        self.assertEqual(str(self.reason), "Test Reason")


class CollectModelTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='testmodelcollectuser', password='12345', email='test@test.ru')
        self.reason = Reason.objects.create(title="Test Reason")

    def test_create_collect(self):
        collect = Collect.objects.create(
            author=self.user,
            title="Test Collect",
            reason=self.reason,
            description="Test description",
            planned_amount=100.00
        )
        self.assertEqual(collect.title, "Test Collect")

    def test_str_method(self):
        collect = Collect.objects.create(
            author=self.user,
            title="Test Collect",
            reason=self.reason,
            description="Test description",
            planned_amount=100.00
        )
        self.assertEqual(str(collect), "Test Collect")


class PaymentModelTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='testmodelpaymentuser', password='12345')
        self.reason = Reason.objects.create(title="Test Reason")
        self.collect = Collect.objects.create(
            author=self.user,
            title="Test Collect",
            reason=self.reason,
            description="Test description",
            planned_amount=100.00
        )

    def test_create_payment(self):
        payment = Payment.objects.create(
            user=self.user,
            title="Test Payment",
            description="Test description",
            amount=10.00,
            collect=self.collect
        )
        self.assertEqual(payment.amount, 10.00)

    def test_str_method(self):
        payment = Payment.objects.create(
            user=self.user,
            title="Test Payment",
            description="Test description",
            amount=10.55,
            collect=self.collect
        )
        self.assertEqual(str(payment), "10.55 от testmodelpaymentuser для Test Collect")

    def test_min_value_validator(self):
        serializer = PaymentSerializer(data={
            'user': self.user.id,
            'title': "Test Payment",
            'description': "Test description",
            'amount': 0.00,
            'collect': self.collect.id
        })
        with self.assertRaises(serializers.ValidationError):
            serializer.is_valid(raise_exception=True)
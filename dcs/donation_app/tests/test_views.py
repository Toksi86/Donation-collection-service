from django.contrib.auth import get_user_model
from django.urls import reverse
from donation_app.models import Reason, Collect, Payment
from rest_framework.test import APITestCase, APIClient

User = get_user_model()


class PaymentViewSetTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testviewpaymentuser', password='12345')
        self.client.force_authenticate(user=self.user)
        self.reason = Reason.objects.create(title="Test Reason")
        self.collect = Collect.objects.create(
            author=self.user,
            title="Test Collect",
            reason=self.reason,
            description="Test description",
            planned_amount=100.00
        )
        self.payment_data = {
            'title': "Test Payment",
            'description': "Test description",
            'amount': 10.00,
            'collect': self.collect.id
        }

    def test_create_payment(self):
        response = self.client.post(reverse('payment-list'), self.payment_data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Payment.objects.count(), 1)

    def test_list_payments(self):
        self.client.post(reverse('payment-list'), self.payment_data, format='json')
        response = self.client.get(reverse('payment-list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)


class CollectViewSetTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testviewcollectuser', password='12345')
        self.client.force_authenticate(user=self.user)
        self.reason = Reason.objects.create(title="Test Reason")
        self.collect_data = {
            'title': "Test Collect",
            'reason': self.reason.id,
            'description': "Test description",
            'planned_amount': 100.00
        }

    def test_create_collect(self):
        response = self.client.post(reverse('collect-list'), self.collect_data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Collect.objects.count(), 1)

    def test_list_collects(self):
        self.client.post(reverse('collect-list'), self.collect_data, format='json')
        response = self.client.get(reverse('collect-list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_get_payments_by_collect(self):
        collect = Collect.objects.create(
            author=self.user,
            title="Test Collect",
            reason=self.reason,
            description="Test description",
            planned_amount=100.00
        )
        Payment.objects.create(
            user=self.user,
            title="Test Payment",
            description="Test description",
            amount=10.00,
            collect=collect
        )
        response = self.client.get(reverse('collect-payments-by-collect', kwargs={'pk': collect.id}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)


class AuthenticationTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_data = {
            'username': 'testviewauthuser',
            'password': '12345',
        }

        response = self.client.post(reverse('register'), self.user_data, format='json')
        self.assertEqual(response.status_code, 201)
        self.token = response.data['token']

    def test_register(self):
        self.assertIsNotNone(self.token)

    def test_login(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token}')
        response = self.client.post(reverse('login'), self.user_data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('token', response.data)

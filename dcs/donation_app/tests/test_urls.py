from django.test import TestCase, Client


class StaticURLTests(TestCase):
    def setUp(self):
        self.guest_client = Client()

    def test_homepage(self):
        response = self.guest_client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_payments(self):
        response = self.guest_client.get('/payments/')
        self.assertEqual(response.status_code, 200)

    def test_collects(self):
        response = self.guest_client.get('/collects/')
        self.assertEqual(response.status_code, 200)

    def test_reasons(self):
        response = self.guest_client.get('/reasons/')
        self.assertEqual(response.status_code, 200)


class UnauthorizedPostRequestsTest(TestCase):
    def setUp(self):
        self.guest_client = Client()

    def test_unauthorized_post_to_payments(self):
        response = self.guest_client.post('/payments/')
        self.assertEqual(response.status_code, 401)

    def test_unauthorized_post_to_collects(self):
        response = self.guest_client.post('/collects/')
        self.assertEqual(response.status_code, 401)

    def test_unauthorized_post_to_reasons(self):
        response = self.guest_client.post('/reasons/')
        self.assertEqual(response.status_code, 401)

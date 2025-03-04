from django.test import TestCase, Client
from django.urls import reverse

class DocsViewTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_docs_view(self):
        response = self.client.get(reverse('api_docs'))
        self.assertEqual(response.status_code, 200)

    def tearDown(self):
        return super().tearDown()

    
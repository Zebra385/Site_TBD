from django.test import TestCase, RequestFactory
from django.urls import reverse

class AccueilPageTestCase(TestCase):
    """
    Test that accueil page returns a 200 if the item exists.
    """
    def test_accueil_page(self):
        response = self.client.get(reverse('accueil'))
        self.assertEqual(response.status_code, 200)
from django.core.urlresolvers import reverse
from django.test import TestCase


class FooterViewTests(TestCase):
    def test_contact_page_view(self):
        response = self.client.get(reverse('footer:contact_page'))
        self.assertEqual(response.status_code, 200)

    def test_tnc_view(self):
        response = self.client.get(reverse('footer:tnc'))
        self.assertEqual(response.status_code, 200)

    def test_privacy_policy_view(self):
        response = self.client.get(reverse('footer:privacy_policy'))
        self.assertEqual(response.status_code, 200)
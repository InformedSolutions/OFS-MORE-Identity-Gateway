import os

from django.conf import settings
from django.test import TestCase


class IdentityGatewayTests(TestCase):
    def test_get_request_returns_404_for_nonexistent_email(self):
        """
        Test that making a query for an email that is not associated with an account returns a 404 response code.
        """
        prefix = settings.PUBLIC_APPLICATION_URL
        response = self.client.get(prefix + '/api/v1/user/?email=nonexistentemail%40test.com')

        self.assertEqual(response.status_code, 404)

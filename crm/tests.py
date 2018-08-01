from django.test import TestCase
from crm.models import User


class UserTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="test@example.com",
            password="password",
            first_name="test",
            last_name="test")

    def test_is_site_user(self):
        """
        User.is_site_user defaults to True when creating users with no
        organization.
        """
        self.assertTrue(self.user.is_site_user)

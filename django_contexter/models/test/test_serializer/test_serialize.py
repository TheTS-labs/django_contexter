"""Test dynamic serializer."""

from django.contrib.auth.models import User
from django.test import TestCase

from django_contexter.models.serializer import Serializer


class SerializerTestCase(TestCase):
    """Test dynamic serializer."""

    def setUp(self):  # noqa: D102
        self.user_attributes = {
            "username": "john",
            "email": "lennon@thebeatles.com",
            "password": "johnpassword",
        }

        self.user_serialized = {"username": "john", "email": "lennon@thebeatles.com"}

    def test_serializer(self):
        """Test work of dynamic serializer."""
        self.user = User.objects.create_user(**self.user_attributes)

        self.serializer = Serializer(
            self.user,
            context={"model": User, "fields": ["username", "email"]},
        )

        self.assertEqual(self.serializer.data, self.user_serialized)

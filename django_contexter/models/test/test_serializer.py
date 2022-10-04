from django.contrib.auth.models import User
from django.test import TestCase

from ..serializer import Serializer


class SerializerTestCase(TestCase):
    def setUp(self):
        self.user_attributes = {
            "username": "john",
            "email": "lennon@thebeatles.com",
            "password": "johnpassword",
        }

        self.user_serialized = {"username": "john", "email": "lennon@thebeatles.com"}

        self.user = User.objects.create_user(**self.user_attributes)
        self.serializer = Serializer(
            self.user,
            context={"model": User, "fields": ["username", "email"]},
        )

    def test_serializer(self):
        """Test work of custom serializer"""
        self.assertEqual(self.serializer.data, self.user_serialized)

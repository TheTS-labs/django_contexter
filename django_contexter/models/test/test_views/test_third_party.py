"""Test third-party functions of views.py."""
from django.test import TestCase

from django_contexter.models import views


class ThirdPartyTestCase(TestCase):
    """Test third-party functions of views.py."""

    def test_exclude_keys(self):
        """Test esclude_keys function."""
        full = {"1": 1, "2": 2, "3": 3}
        expected = {"1": 1, "3": 3}

        self.assertEqual(expected, views.Index()._exclude_keys(full, ["2"]))

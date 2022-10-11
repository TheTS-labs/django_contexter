"""Test the compliance of the method Access Policy."""

from django.test import TestCase

from django_contexter.models.errors.reject_error import RejectError
from django_contexter.models.method_types import ALL_METHODS, ALL_SAFE_METHODS, ALL_UNSAFE_METHODS
from django_contexter.models.get_model import GetModel
from django_contexter.models.test.test_model.configs import MethodsConfigs

# ? Why need noqa: WPS440?
# * method isn't overlapped
# * These local variable used in it own for loop


class MethodsTestCase(TestCase, MethodsConfigs):
    """Test the compliance of the method Access Policy."""

    def test_local_access_method(self):
        """Check whether the method complies with the Access Policy for the local configuration."""
        with self.settings(
            CONTEXTER_ACCESS_POLICY=self.configs["test_local_reject_method"],
        ):
            model = GetModel("auth.Permission")

            for method in ALL_METHODS - ALL_SAFE_METHODS:
                with self.assertRaises(RejectError):
                    model.check_method(method)

            for method in ALL_METHODS - ALL_UNSAFE_METHODS:
                self.assertTrue(model.check_method(method))

    def test_global_access_method(self):
        """Check whether the method complies with the Access Policy for the global configuration."""
        with self.settings(
            CONTEXTER_ACCESS_POLICY=self.configs["test_global_reject_method"],
        ):
            model = GetModel("auth.Permission")

            for method in ALL_METHODS - ALL_SAFE_METHODS:
                with self.assertRaises(RejectError):
                    model.check_method(method)

            for method in ALL_METHODS - ALL_UNSAFE_METHODS:
                self.assertTrue(model.check_method(method))

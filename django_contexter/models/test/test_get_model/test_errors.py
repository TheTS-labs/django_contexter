"""Test error handling."""

from django.test import TestCase, override_settings

from django_contexter.models.errors.request_error import RequestError
from django_contexter.models.get_model import GetModel
from django_contexter.models.method_lists import ALL_SAFE_METHODS


class ModelErrorsTestCase(TestCase):
    """Test error handling."""

    config = {
        "allow_methods": ALL_SAFE_METHODS,
        "allow_models": ["model_NotExists", "model.NotExists"],
        "reject_models": [],
    }

    @override_settings(CONTEXTER_ACCESS_POLICY=config)
    def test_lookup_error(self):
        """Test LookupError handling."""
        # Sus.
        self.assertRaises(
            RequestError,
            self._try_model,
            "modelNot.Exists",
        )

    @override_settings(CONTEXTER_ACCESS_POLICY=config)
    def test_wrong_paths(self):
        """Test ValueError handling."""
        self.assertRaises(
            RequestError,
            self._try_model,
            "model.Not.Exists",
        )

        self.assertRaises(
            RequestError,
            self._try_model,
            "model_NotExists",
        )

    def _try_model(self, model_name):
        if GetModel(model_name).model:
            self.fail("Something has been returned")

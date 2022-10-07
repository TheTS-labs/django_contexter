"""Test third-party functions of views.py."""
from django.test import TestCase

from django_contexter.models.errors.configuration_error import ConfigurationError
from django_contexter.models.errors.err_codes import REJECT_ERROR, SERVER_WRONG_CONFIG
from django_contexter.models.errors.reject_error import RejectError
from django_contexter.models.errors.request_error import RequestError
from django_contexter.models.views import error_handler, exclude_keys


class ThirdPartyTestCase(TestCase):
    """Test third-party functions of views.py."""

    def test_error_handler_decorator(self):
        """Test error handler decorator."""
        test_cases = [
            [
                error_handler(self._to_be_decorated_reject),
                "Request was rejected(Unknown Model). Reason: Unknown Reason",
                REJECT_ERROR,
                403,
            ],
            [
                error_handler(self._to_be_decorated_config),
                "Test message",
                SERVER_WRONG_CONFIG,
                500,
            ],
            [
                error_handler(self._to_be_decorated_request),
                "Unknown Error",
                -1,
                500,
            ],
        ]

        for index, test_case in enumerate(test_cases):
            function = test_case[index][0]
            self.assertEqual(function().data["err_msg"], test_case[index][1])
            self.assertEqual(function().data["err_code"], test_case[index][2])
            self.assertEqual(function().status_code, test_case[index][3])

    def test_exclude_keys(self):
        """Test esclude_keys function."""
        full = {"1": 1, "2": 2, "3": 3}
        expected = {"1": 1, "3": 3}

        self.assertEqual(expected, exclude_keys(full, ["2"]))

    def _to_be_decorated_reject(self):
        raise RejectError()

    def _to_be_decorated_config(self):
        raise ConfigurationError("Test message")

    def _to_be_decorated_request(self):
        raise RequestError()

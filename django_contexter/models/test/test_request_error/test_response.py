"""Test RequestError, base error."""

from django.test import TestCase
from rest_framework.response import Response
from rest_framework.status import HTTP_500_INTERNAL_SERVER_ERROR, HTTP_501_NOT_IMPLEMENTED

from django_contexter.models.errors.request_error import RequestError


class RequestErrorResponseTestCase(TestCase):
    """Test RequestError, base error."""

    def test_default_response(self):
        """Test default response, fails if default message changed."""
        err = RequestError()
        expected = Response(
            {"err_code": -1, "err_msg": "Unknown Error"},
            status=HTTP_500_INTERNAL_SERVER_ERROR,
        )

        self.assertEqual(err.response.data, expected.data)
        self.assertEqual(err.response.status_code, expected.status_code)

    def test_custom_response(self):
        """Test custom response."""
        err = RequestError("Test message", 0, HTTP_501_NOT_IMPLEMENTED)
        expected = Response(
            {"err_code": 0, "err_msg": "Test message"}, status=HTTP_501_NOT_IMPLEMENTED,
        )

        self.assertEqual(err.response.data, expected.data)
        self.assertEqual(err.response.status_code, expected.status_code)

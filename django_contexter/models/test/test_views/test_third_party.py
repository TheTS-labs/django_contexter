from django.conf import settings
from django.test import RequestFactory, TestCase
from django_contexter.models.change_result import ChangeResult

from django_contexter.models.method_types import ALL_METHODS, ALL_SAFE_METHODS

from ...errors.err_codes import (
    FIELD_ERROR,
    FUNCTION_DOES_NOT_EXIST_IN_QUERYSET_API,
    NO_MANDATORY_PARAMETER_MODELNAME,
    REJECT_ERROR,
    SERVER_WRONG_CONFIG,
)

from ...errors.request_error import RequestError
from ...views import Error_Handler, exclude_keys, index

from ...errors.configuration_error import ConfigurationError

from ...errors.reject_error import RejectError

from django.contrib.auth.models import Permission
from ...serializer import Serializer


class ThirdPartyTestCase(TestCase):
    def test_error_handler_decorator(self):
        def to_be_decorated_reject():
            raise RejectError()

        def to_be_decorated_config():
            raise ConfigurationError("Test message")

        def to_be_decorated_request():
            raise RequestError()

        decorators = [
            Error_Handler(to_be_decorated_reject),
            Error_Handler(to_be_decorated_config),
            Error_Handler(to_be_decorated_request),
        ]
        messages = [
            "Request was rejected(Unknown Model). Reason: Unknown Reason",
            "Test message",
            "Unknown Error",
        ]
        codes = [REJECT_ERROR, SERVER_WRONG_CONFIG, -1]
        statuses = [403, 500, 500]

        for decorator, message, code, status in zip(
            decorators, messages, codes, statuses
        ):
            self.assertEqual(decorator().data["err_msg"], message)
            self.assertEqual(decorator().data["err_code"], code)
            self.assertEqual(decorator().status_code, status)

    def test_exclude_keys(self):
        full = {"1": 1, "2": 2, "3": 3}
        expected = {"1": 1, "3": 3}

        self.assertEqual(expected, exclude_keys(full, ["2"]))

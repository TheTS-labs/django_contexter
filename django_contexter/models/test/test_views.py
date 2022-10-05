from django.conf import settings
from django.test import RequestFactory, TestCase
from django_contexter.models.change_result import ChangeResult

from django_contexter.models.method_types import ALL_METHODS, ALL_SAFE_METHODS

from ..errors.err_codes import (
    FIELD_ERROR,
    FUNCTION_DOES_NOT_EXIST_IN_QUERYSET_API,
    NO_MANDATORY_PARAMETER_MODELNAME,
    REJECT_ERROR,
    SERVER_WRONG_CONFIG,
)

from ..errors.request_error import RequestError
from ..views import Error_Handler, exclude_keys, index

from ..errors.configuration_error import ConfigurationError

from ..errors.reject_error import RejectError

from django.contrib.auth.models import Permission
from ..serializer import Serializer


class ViewsTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def changeConfiguration(self, conf):
        settings.CONTEXTER_ACCESS_POLICY = conf

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

    def test_call_without_modelName(self):
        request = self.factory.get("".join(["/api/models/"]))
        response = index(request)

        self.assertEqual(response.data["err_code"], NO_MANDATORY_PARAMETER_MODELNAME)

    def test_call_with_modelName(self):
        self.changeConfiguration(
            {
                "allow_methods": ALL_SAFE_METHODS,
                "allow_models": "__all__",
                "reject_models": [],
            }
        )

        request = self.factory.get(
            "".join(["/api/models/", "?modelName=auth.Permission"])
        )
        objects = Permission.objects
        serialized = Serializer(
            objects, many=True, context={"model": Permission, "fields": "__all__"}
        )
        response = index(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, serialized.data)

    def test_all_call(self):
        self.changeConfiguration(
            {
                "allow_methods": ALL_SAFE_METHODS,
                "allow_models": "__all__",
                "reject_models": [],
            }
        )

        request = self.factory.get(
            "".join(["/api/models/", "?modelName=auth.Permission", "&all"])
        )
        objects = Permission.objects.all()
        serialized = Serializer(
            objects, many=True, context={"model": Permission, "fields": "__all__"}
        )
        response = index(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, serialized.data)

    def test_get_call(self):
        self.changeConfiguration(
            {
                "allow_methods": ALL_SAFE_METHODS,
                "allow_models": "__all__",
                "reject_models": [],
            }
        )

        request = self.factory.get(
            "".join(
                ["/api/models/", "?modelName=auth.Permission", "&all", '&get={"pk": 1}']
            )
        )
        objects = Permission.objects.all().get(pk=1)
        serialized = Serializer(
            objects, many=False, context={"model": Permission, "fields": "__all__"}
        )
        response = index(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, serialized.data)

    def test_check_method(self):
        self.changeConfiguration(
            {
                "allow_methods": ALL_SAFE_METHODS,
                "allow_models": "__all__",
                "reject_models": [],
            }
        )

        for method in ALL_METHODS - ALL_SAFE_METHODS:
            request = self.factory.get(
                "".join(["/api/models/", "?modelName=auth.Permission", f"&{method}"])
            )
            response = index(request)

            self.assertEqual(response.status_code, 403)
            self.assertEqual(response.data["err_code"], REJECT_ERROR)

    def test_field_error(self):
        self.changeConfiguration(
            {
                "allow_methods": ALL_SAFE_METHODS,
                "allow_models": "__all__",
                "reject_models": [],
            }
        )

        request = self.factory.get(
            "".join(
                [
                    "/api/models/",
                    "?modelName=auth.Permission",
                    "&all",
                    '&get={"pk": 9999}',
                ]
            )
        )
        response = index(request)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["err_code"], FIELD_ERROR)

    def test_attr_error(self):
        self.changeConfiguration(
            {
                "allow_methods": "__any__",
                "allow_models": "__all__",
                "reject_models": [],
            }
        )

        request = self.factory.get(
            "".join(
                [
                    "/api/models/",
                    "?modelName=auth.Permission",
                    "&all",
                    "&commandNotExists",
                ]
            )
        )
        response = index(request)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.data["err_code"], FUNCTION_DOES_NOT_EXIST_IN_QUERYSET_API
        )
        self.assertEqual(
            response.data["err_msg"],
            "No function named 'commandNotExists' in QuerySet API",
        )

    def test_hide(self):
        self.changeConfiguration(
            {
                "allow_methods": ALL_METHODS,
                "allow_models": "__all__",
                "reject_models": [],
                "auth.Permission": {
                    "hidden_fields": ["codename"],
                    "allow_methods": ALL_METHODS,
                },
            }
        )

        request = self.factory.get(
            "".join(["/api/models/", "?modelName=auth.Permission", "&all"])
        )
        response = index(request)

        changer = ChangeResult(
            {"hidden_fields": ["codename"], "allow_methods": ALL_METHODS},
            Permission,
            None,
        )

        records = Permission.objects.all()
        fixed_fields = changer.fix_fields(records.all())
        serialized = Serializer(
            fixed_fields, many=True, context={"model": Permission, "fields": "__all__"}
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, serialized.data)

from django.conf import settings
from django.test import RequestFactory, TestCase
from django_contexter.models.change_result import ChangeResult

from django_contexter.models.method_types import ALL_METHODS, ALL_SAFE_METHODS
from django_contexter.models.test.test_views.configs import Configs

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


class ViewsMainTestCase(TestCase, Configs):
    def setUp(self):
        self.factory = RequestFactory()

    def test_call_without_modelName(self):
        request = self.factory.get("".join(["/api/models/"]))
        response = index(request)

        self.assertEqual(response.data["err_code"], NO_MANDATORY_PARAMETER_MODELNAME)

    def test_call_with_modelName(self):
        with self.settings(
            CONTEXTER_ACCESS_POLICY=self.configs["test_call_with_modelName"]
        ):
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
        with self.settings(CONTEXTER_ACCESS_POLICY=self.configs["test_all_call"]):
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
        with self.settings(CONTEXTER_ACCESS_POLICY=self.configs["test_get_call"]):
            request = self.factory.get(
                "".join(
                    [
                        "/api/models/",
                        "?modelName=auth.Permission",
                        "&all",
                        '&get={"pk": 1}',
                    ]
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
        with self.settings(CONTEXTER_ACCESS_POLICY=self.configs["test_check_method"]):
            for method in ALL_METHODS - ALL_SAFE_METHODS:
                request = self.factory.get(
                    "".join(
                        ["/api/models/", "?modelName=auth.Permission", f"&{method}"]
                    )
                )
                response = index(request)

                self.assertEqual(response.status_code, 403)
                self.assertEqual(response.data["err_code"], REJECT_ERROR)

    def test_field_error(self):
        with self.settings(CONTEXTER_ACCESS_POLICY=self.configs["test_field_error"]):
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
        with self.settings(CONTEXTER_ACCESS_POLICY=self.configs["test_attr_error"]):
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
        with self.settings(CONTEXTER_ACCESS_POLICY=self.configs["test_hide"]):
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
                fixed_fields,
                many=True,
                context={"model": Permission, "fields": "__all__"},
            )

            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.data, serialized.data)

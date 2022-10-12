"""Contains "call" tests."""

from django.contrib.auth.models import Permission
from django.test import RequestFactory, TestCase
from rest_framework import status

from django_contexter.models.errors.err_codes import NO_MANDATORY_PARAMETER_MODELNAME
from django_contexter.models.serializer import Serializer
from django_contexter.models.test.test_views.configs import Configs
from django_contexter.models.views import index


class CallsTestCase(TestCase, Configs):
    """Part of ViewsMainTestCase: contains all "call" tests."""

    def setUp(self):  # noqa: D102
        self.factory = RequestFactory()

    def test_call_without_model_name(self):
        """Test call without modelName, expect error."""
        response = self._get_response("".join(["/api/models/"]))

        self.assertEqual(response.data["err_code"], NO_MANDATORY_PARAMETER_MODELNAME)

    def test_call_with_model_name(self):
        """Test call with modelName, expect all records."""
        with self.settings(CONTEXTER_ACCESS_POLICY=self.configs["test_call_with_modelName"]):
            response = self._get_response("".join([
                "/api/models/",
                "?modelName=auth.Permission",
            ]))
            model_objects = Permission.objects
            serialized = Serializer(
                model_objects, many=True, context={"model": Permission, "fields": "__all__"},
            )

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.data, serialized.data)

    def test_all_call(self):
        """Test "all" call, expect all records."""
        with self.settings(CONTEXTER_ACCESS_POLICY=self.configs["test_all_call"]):
            response = self._get_response("".join([
                "/api/models/",
                "?modelName=auth.Permission",
                "&all",
            ]))
            model_objects = Permission.objects.all()
            serialized = Serializer(
                model_objects, many=True, context={"model": Permission, "fields": "__all__"},
            )

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.data, serialized.data)

    def test_get_call(self):
        """Test "get" call, expect ONLY ONE records."""
        with self.settings(CONTEXTER_ACCESS_POLICY=self.configs["test_get_call"]):
            response = self._get_response("".join([
                "/api/models/",
                "?modelName=auth.Permission",
                "&all",
                '&get={"pk": 1}',
            ]))
            model_objects = Permission.objects.all().get(pk=1)
            serialized = Serializer(
                model_objects, many=False, context={"model": Permission, "fields": "__all__"},
            )

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.data, serialized.data)

    def _get_response(self, path):
        request = self.factory.get(path)

        return index(request)

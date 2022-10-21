"""Test index function from views.py."""

from django.contrib.auth.models import Permission
from django.test import RequestFactory, TestCase
from rest_framework import status

from django_contexter.models import views
from django_contexter.models.change_result import ChangeResult
from django_contexter.models.errors.err_codes import FIELD_ERROR, FUNCTION_DOES_NOT_EXIST_IN_QUERYSET_API, REJECT_ERROR
from django_contexter.models.method_types import ALL_METHODS, ALL_SAFE_METHODS
from django_contexter.models.serializer import Serializer
from django_contexter.models.test.test_views.configs import Configs


class MainTestCase(TestCase, Configs):
    """Test index function from views.py."""

    def setUp(self):  # noqa: D102
        self.factory = RequestFactory()

    def test_check_method(self):
        """Test check_method function."""
        with self.settings(CONTEXTER_ACCESS_POLICY=self.configs["test_check_method"]):
            for method in ALL_METHODS - ALL_SAFE_METHODS:
                response = self._get_response("".join([
                    "/api/models/", "?modelName=auth.Permission", f"&{method}",
                ]))

                self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
                self.assertEqual(response.data["err_code"], REJECT_ERROR)

    def test_field_error(self):
        """Test FieldError handling."""
        with self.settings(CONTEXTER_ACCESS_POLICY=self.configs["test_field_error"]):
            response = self._get_response("".join([
                "/api/models/",
                "?modelName=auth.Permission",
                "&all",
                '&get={"pk": 9999}',
            ]))

            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertEqual(response.data["err_code"], FIELD_ERROR)

    def test_attr_error(self):
        """Test AttributeError handling."""
        with self.settings(CONTEXTER_ACCESS_POLICY=self.configs["test_attr_error"]):
            response = self._get_response("".join([
                "/api/models/",
                "?modelName=auth.Permission",
                "&all",
                "&commandNotExists",
            ]))

            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertEqual(response.data["err_code"], FUNCTION_DOES_NOT_EXIST_IN_QUERYSET_API)
            self.assertTrue("commandnotexists" in response.data["err_msg"].lower())

    def test_hide(self):
        """Test hiding feature."""
        with self.settings(CONTEXTER_ACCESS_POLICY=self.configs["test_hide"]):
            response = self._get_response("".join([
                "/api/models/", "?modelName=auth.Permission", "&all",
            ]))

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

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.data, serialized.data)

    def _get_response(self, path):
        request = self.factory.get(path)

        return views.Index.as_view()(request)

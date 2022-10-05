from django.test import TestCase, override_settings

from django_contexter.models.errors.request_error import RequestError
from django_contexter.models.test.test_model.configs import Errors_Config
from ...model import Model


class ModelErrorsTestCase(TestCase):
    @override_settings(CONTEXTER_ACCESS_POLICY=Errors_Config.config())
    def test_lookup_error(self):
        with self.assertRaises(RequestError):
            try:
                Model("model.NotExists").model
            except RequestError as exc:
                raise exc

    @override_settings(CONTEXTER_ACCESS_POLICY=Errors_Config.config())
    def test_wrong_paths(self):
        with self.assertRaises(RequestError):
            try:
                Model("model.Not.Exists").model
            except RequestError as exc:
                raise exc

        with self.assertRaises(RequestError):
            try:
                Model("model_NotExists").model
            except RequestError as exc:
                raise exc

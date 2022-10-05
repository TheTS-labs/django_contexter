from django.conf import settings
from django.contrib.auth.models import Permission, User
from django.test import TestCase

from django_contexter.models.errors.request_error import RequestError
from django_contexter.models.method_types import (
    ALL_METHODS,
    ALL_SAFE_METHODS,
    ALL_UNSAFE_METHODS,
)
from django_contexter.models.test.test_model.configs import Methods_Configs

from ...errors.configuration_error import ConfigurationError
from ...errors.reject_error import RejectError
from ...model import Model


class ModelTestCase(TestCase, Methods_Configs):
    def test_local_reject_method(self):
        with self.settings(
            CONTEXTER_ACCESS_POLICY=self.configs["test_local_reject_method"]
        ):
            model = Model("auth.Permission")

            for method in ALL_METHODS - ALL_SAFE_METHODS:
                with self.assertRaises(RejectError):
                    model.check_method(method)

            with self.assertRaises(RejectError):
                model.check_method("Method Not Exist")

            for method in ALL_METHODS - ALL_UNSAFE_METHODS:
                self.assertEqual(model.check_method(method), True)

    def test_global_reject_method(self):
        with self.settings(
            CONTEXTER_ACCESS_POLICY=self.configs["test_global_reject_method"]
        ):
            model = Model("auth.Permission")

            for method in ALL_METHODS - ALL_SAFE_METHODS:
                with self.assertRaises(RejectError):
                    model.check_method(method)

            for method in ALL_METHODS - ALL_UNSAFE_METHODS:
                self.assertEqual(model.check_method(method), True)

    # def test_any(self):
    #     with self.settings(CONTEXTER_ACCESS_POLICY=self.configs["test_any"]):
    #         model = Model("auth.Permission")

    #         with self.assertRaises(RequestError):
    #             model.check_method("Method Not Exist")

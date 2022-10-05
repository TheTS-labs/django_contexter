from django.conf import settings
from django.contrib.auth.models import Permission, User
from django.test import TestCase

from django_contexter.models.errors.request_error import RequestError
from django_contexter.models.method_types import (
    ALL_METHODS,
    ALL_SAFE_METHODS,
    ALL_UNSAFE_METHODS,
)

from ..errors.configuration_error import ConfigurationError
from ..errors.reject_error import RejectError
from ..model import Model


class ModelTestCase(TestCase):
    def changeConfiguration(self, conf):
        settings.CONTEXTER_ACCESS_POLICY = conf

    def test_accesssed_path(self):
        policy = {
            "allow_methods": ALL_METHODS,
            "allow_models": ["auth.Permission"],
            "reject_models": "__remaining__",
        }

        self.changeConfiguration(policy)

        model = Model("auth.Permission")

        self.assertEqual(model.props, None)
        self.assertEqual(model.model, Permission)

    def test_wrong_config_all(self):
        policy = {
            "allow_methods": ALL_METHODS,
            "allow_models": "__all__",
            "reject_models": "__all__",
        }

        self.changeConfiguration(policy)

        with self.assertRaises(ConfigurationError):
            try:
                Model("auth.Permission").model
            except ConfigurationError as exc:
                raise exc

    def test_wrong_config_one_model(self):
        policy = {
            "allow_methods": ALL_METHODS,
            "allow_models": ["auth.Permission"],
            "reject_models": ["auth.Permission"],
        }

        self.changeConfiguration(policy)

        with self.assertRaises(ConfigurationError):
            try:
                Model("auth.Permission").model
            except ConfigurationError as exc:
                raise exc

    def test_rejected_model(self):
        policy = {
            "allow_methods": ALL_METHODS,
            "allow_models": "__remaining__",
            "reject_models": ["auth.Permission"],
        }

        self.changeConfiguration(policy)

        with self.assertRaises(RejectError):
            try:
                Model("auth.Permission").model
            except RejectError as exc:
                raise exc

        self.assertEqual(Model("auth.User").model, User)

    def test_all_with_remaining(self):
        policy = {
            "allow_methods": ALL_METHODS,
            "allow_models": "__all__",
            "reject_models": "__remaining__",
        }

        self.changeConfiguration(policy)

        with self.assertRaises(ConfigurationError):
            try:
                Model("auth.Permission").model
            except ConfigurationError as exc:
                raise exc

    def test_lookup_error(self):
        with self.assertRaises(RequestError):
            try:
                Model("model.NotExists").model
            except RequestError as exc:
                raise exc

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

    def test_empty_props(self):
        policy = {
            "allow_methods": ALL_METHODS,
            "allow_models": "__remaining__",
            "reject_models": "__undeclared__",
            "auth.Permission": {"testProps": True},
        }

        self.changeConfiguration(policy)

        self.assertEqual(Model("auth.Permission").props, {"testProps": True})

    def test_reject_method(self):
        policy = {
            "allow_methods": ALL_METHODS,
            "allow_models": "__remaining__",
            "reject_models": "__undeclared__",
            "auth.Permission": {
                "allow_methods": ALL_SAFE_METHODS,
            },
        }

        self.changeConfiguration(policy)

        model = Model("auth.Permission")

        for method in ALL_METHODS - ALL_SAFE_METHODS:
            with self.assertRaises(RejectError):
                model.check_method(method)

        with self.assertRaises(RejectError):
            model.check_method("Method Not Exist")

        for method in ALL_METHODS - ALL_UNSAFE_METHODS:
            self.assertEqual(model.check_method(method), True)

    def test_reject_method_with_empty_props(self):
        policy = {
            "allow_methods": ALL_SAFE_METHODS,
            "allow_models": "__all__",
            "reject_models": [],
        }

        self.changeConfiguration(policy)

        model = Model("auth.Permission")

        for method in ALL_METHODS - ALL_SAFE_METHODS:
            with self.assertRaises(RejectError):
                model.check_method(method)

        with self.assertRaises(RejectError):
            model.check_method("Method Not Exist")

        for method in ALL_METHODS - ALL_UNSAFE_METHODS:
            self.assertEqual(model.check_method(method), True)

    def test_part__remaining_and_not_allowed(self):
        policy = {
            "allow_methods": ALL_SAFE_METHODS,
            "allow_models": ["auth.User"],
            "reject_models": "__remaining__",
        }

        self.changeConfiguration(policy)

        with self.assertRaises(RejectError):
            try:
                Model("auth.Permission").model
            except RejectError as exc:
                raise exc

    def test_all_allowed_methods(self):
        policy = {
            "allow_methods": ALL_SAFE_METHODS,
            "allow_models": "__all__",
            "reject_models": [],
        }

        self.changeConfiguration(policy)

        model = Model("auth.Permission")

        for method in ALL_METHODS - ALL_UNSAFE_METHODS:
            self.assertEqual(model.check_method(method), True)

        with self.assertRaises(RejectError):
            model.check_method("Method Not Exist")

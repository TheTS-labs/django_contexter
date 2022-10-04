from django.conf import settings
from django.contrib.auth.models import Permission
from django.test import TestCase

from django_contexter.models.errors.request_error import RequestError

from ..errors.configuration_error import ConfigurationError
from ..errors.reject_error import RejectError
from ..get_model import GetModel


class GetModelTestCase(TestCase):
    def changeConfiguration(self, conf):
        settings.CONTEXTER_ACCESS_POLICY = conf

    def test_accesssed_path(self):
        policy = {
            "allow_methods": "__all__",
            "allow_models": ["auth.Permission"],
            "reject_models": "__remaining__",
        }

        self.changeConfiguration(policy)

        gm = GetModel("auth.Permission")

        self.assertEqual(gm.props, None)
        self.assertEqual(gm.model, Permission)

    def test_wrong_config_all(self):
        policy = {
            "allow_methods": "__all__",
            "allow_models": "__all__",
            "reject_models": "__all__",
        }

        self.changeConfiguration(policy)

        with self.assertRaises(ConfigurationError):
            try:
                GetModel("auth.Permission").model
            except ConfigurationError as exc:
                raise exc

    def test_wrong_config_one_model(self):
        policy = {
            "allow_methods": "__all__",
            "allow_models": ["auth.Permission"],
            "reject_models": ["auth.Permission"],
        }

        self.changeConfiguration(policy)

        with self.assertRaises(ConfigurationError):
            try:
                GetModel("auth.Permission").model
            except ConfigurationError as exc:
                raise exc

    def test_rejected_model(self):
        policy = {
            "allow_methods": "__all__",
            "allow_models": [""],
            "reject_models": ["auth.Permission"],
        }

        self.changeConfiguration(policy)

        with self.assertRaises(RejectError):
            try:
                GetModel("auth.Permission").model
            except RejectError as exc:
                raise exc

    def test_all_with_remaining(self):
        policy = {
            "allow_methods": "__all__",
            "allow_models": "__all__",
            "reject_models": "__remaining__",
        }

        self.changeConfiguration(policy)

        with self.assertRaises(ConfigurationError):
            try:
                GetModel("auth.Permission").model
            except ConfigurationError as exc:
                raise exc

    def test_lookup_error(self):
        with self.assertRaises(RequestError):
            try:
                GetModel("model.NotExists").model
            except RequestError as exc:
                raise exc

    def test_wrong_paths(self):
        with self.assertRaises(RequestError):
            try:
                GetModel("model.Not.Exists").model
            except RequestError as exc:
                raise exc

        with self.assertRaises(RequestError):
            try:
                GetModel("model_NotExists").model
            except RequestError as exc:
                raise exc

    def test_empty_props(self):
        policy = {
            "allow_methods": "__all__",
            "allow_models": "__all__",
            "reject_models": "__undeclared__",
            "auth.Permission": {"testProps": True},
        }

        self.changeConfiguration(policy)

        self.assertEqual(GetModel("auth.Permission").props, {"testProps": True})

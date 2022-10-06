import django
from django.contrib.auth.models import User
from django.test import TestCase
from django_contexter.models.errors.reject_error import RejectError
from django_contexter.models.model import Model
from django_contexter.models.test.test_model.configs import Just_Configs


class ConfigsTestCase(TestCase, Just_Configs):
    def setUp(self):
        self.models = set(
            django.apps.apps.get_models(include_auto_created=True, include_swapped=True)
        )

    def test_allow(self):
        """Test a simple setting that allows everything"""

        with self.settings(CONTEXTER_ACCESS_POLICY=self.configs["test_allow"]):
            for model in self.models:
                self.assertIs(type(Model(model._meta.label).model), type(model))

    def test_reject(self):
        """Test a simple setting that allows everything except auth.User"""

        with self.settings(CONTEXTER_ACCESS_POLICY=self.configs["test_reject"]):
            with self.assertRaises(RejectError):
                try:
                    Model("auth.User")
                except RejectError as exc:
                    raise exc

            for model in self.models - set([User]):
                self.assertIs(type(Model(model._meta.label).model), type(model))

    def test_reject_all(self):
        with self.settings(CONTEXTER_ACCESS_POLICY=self.configs["test_reject_all"]):
            for model in self.models:
                with self.assertRaises(RejectError):
                    try:
                        Model(model._meta.label).model
                    except RejectError as exc:
                        raise exc

    def test_reject_remaining(self):
        with self.settings(
            CONTEXTER_ACCESS_POLICY=self.configs["test_reject_remaining"]
        ):
            with self.assertRaises(RejectError):
                try:
                    for model in self.models - set([User]):
                        self.assertIs(type(Model(model._meta.label).model), type(model))
                except RejectError as exc:
                    raise exc

            self.assertIs(type(Model("auth.User").model), type(User))

    def test_allow_undeclared(self):
        with self.settings(
            CONTEXTER_ACCESS_POLICY=self.configs["test_allow_undeclared"]
        ):
            with self.assertRaises(RejectError):
                try:
                    Model("auth.User")
                except RejectError as exc:
                    raise exc

            for model in self.models - set([User]):
                self.assertIs(type(Model(model._meta.label).model), type(model))

    def test_reject_undeclared(self):
        with self.settings(
            CONTEXTER_ACCESS_POLICY=self.configs["test_reject_undeclared"]
        ):
            with self.assertRaises(RejectError):
                try:
                    for model in self.models - set([User]):
                        self.assertIs(type(Model(model._meta.label).model), type(model))
                except RejectError as exc:
                    raise exc

            self.assertIs(type(Model("auth.User").model), type(User))

    def test_empty_props(self):
        with self.settings(CONTEXTER_ACCESS_POLICY=self.configs["test_emty_props"]):
            self.assertEqual(Model("auth.Permission").props, {"testProps": True})

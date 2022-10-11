import django
from django.contrib.auth.models import User
from django.test import TestCase

from django_contexter.models.errors.reject_error import RejectError
from django_contexter.models.get_model import GetModel
from django_contexter.models.test.test_model.configs import JustConfigs

# ? Why need noqa: WPS437?
# * Because Django doesn't forbid the use of _meta
# https://docs.djangoproject.com/en/4.1/ref/models/meta/


class TestAllow(object):
    """Test "allow" configs."""

    def test_allow(self):
        """Test a simple setting that allows everything."""
        with self.settings(CONTEXTER_ACCESS_POLICY=self.configs["test_allow"]):
            for model in self.models:
                self._assert_model(
                    model=model._meta.label,
                    instance=model,
                )

    def test_allow_undeclared(self):
        """Test a simple setting that allows undeclared models."""
        with self.settings(CONTEXTER_ACCESS_POLICY=self.configs["test_allow_undeclared"]):
            self.assertRaises(
                RejectError,
                self._assert_model,
                model="auth.User",
                instance=User,
            )

            for model in self.models - {User}:
                self._assert_model(
                    model=model._meta.label,
                    instance=model,
                )


class ConfigsTestCase(TestCase, JustConfigs, TestAllow):
    """Test some config situations."""

    def setUp(self):  # noqa: D102
        self.models = set(
            django.apps.apps.get_models(include_auto_created=True, include_swapped=True),
        )

    def test_reject(self):
        """Test a simple setting that allows everything except auth.User."""
        with self.settings(CONTEXTER_ACCESS_POLICY=self.configs["test_reject"]):
            self.assertRaises(
                RejectError,
                self._assert_model,
                model="auth.User",
                instance=User,
            )

            for model in self.models - {User}:
                self._assert_model(model._meta.label, model)

    def test_reject_all(self):
        """Test a setting that rejects everything."""
        with self.settings(CONTEXTER_ACCESS_POLICY=self.configs["test_reject_all"]):
            for model in self.models:
                self.assertRaises(
                    RejectError,
                    self._assert_model,
                    model=model._meta.label,
                    instance=model,
                )

    def test_reject_remaining(self):
        """Test a setting that rejects __remaining__."""
        with self.settings(
            CONTEXTER_ACCESS_POLICY=self.configs["test_reject_remaining"],
        ):
            for model in self.models - {User}:
                self.assertRaises(
                    RejectError,
                    self._assert_model,
                    model=model._meta.label,
                    instance=model,
                )

            self._assert_model("auth.User", User)

    def test_reject_undeclared(self):
        """Test a setting that rejects __undeclared__."""
        with self.settings(CONTEXTER_ACCESS_POLICY=self.configs["test_reject_undeclared"]):
            for model in self.models - {User}:
                self.assertRaises(
                    RejectError,
                    self._assert_model,
                    model=model._meta.label,
                    instance=model,
                )

            self._assert_model("auth.User", User)

    def test_empty_props(self):
        """Sus."""
        with self.settings(CONTEXTER_ACCESS_POLICY=self.configs["test_emty_props"]):
            self.assertEqual(GetModel("auth.Permission").props, {"testProps": True})

    def _assert_model(self, model, instance):
        self.assertIs(type(GetModel(model).model), type(instance))

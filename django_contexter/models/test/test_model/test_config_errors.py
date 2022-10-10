from django.contrib.auth.models import Permission
from django.test import TestCase

from django_contexter.models.errors.configuration_error import ConfigurationError
from django_contexter.models.model import GetModel
from django_contexter.models.test.test_model.configs import ConfigErrorsConfigs


class ModelConfigTestCase(TestCase, ConfigErrorsConfigs):
    """Test configs that raises ConfigurationError."""

    def test_asserts(self):
        """Test configs."""
        for config in self.configs.items():
            with self.settings(CONTEXTER_ACCESS_POLICY=self.configs[config[0]]):
                self.assertRaises(
                    ConfigurationError,
                    self._assert_model,
                    model="auth.Permission",
                    instance=Permission,
                )

    def _assert_model(self, model, instance):
        self.assertIs(type(GetModel(model).model), type(instance))

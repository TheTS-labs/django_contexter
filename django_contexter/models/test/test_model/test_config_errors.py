from django.contrib.auth.models import Permission
from django.test import TestCase
from django_contexter.models.errors.configuration_error import ConfigurationError

from django_contexter.models.model import Model
from django_contexter.models.test.test_model.configs import Config_errors_Configs


class ModelConfigTestCase(TestCase, Config_errors_Configs):
    def test_asserts(self):
        for config in self.configs:
            with self.settings(CONTEXTER_ACCESS_POLICY=self.configs[config]):
                with self.assertRaises(ConfigurationError):
                    try:
                        self.assertIs(
                            type(Model("auth.Permission").model), type(Permission)
                        )
                    except ConfigurationError as exc:
                        raise exc

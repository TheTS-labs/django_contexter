"""Contain config dicts for tests."""

from types import MappingProxyType

from django_contexter.models.method_types import ALL_METHODS, ALL_SAFE_METHODS

SIMPLE_CONFIG = MappingProxyType({
    "allow_methods": ALL_SAFE_METHODS,
    "allow_models": "__all__",
    "reject_models": [],
})


class Configs(object):
    """Contain config dicts for tests."""

    @property
    def configs(self):
        """
        Get config dicts for tests.

        Returns:
            dict: config dicts
        """
        return {
            "test_call_with_modelName": SIMPLE_CONFIG,
            "test_all_call": SIMPLE_CONFIG,
            "test_get_call": SIMPLE_CONFIG,
            "test_check_method": SIMPLE_CONFIG,
            "test_field_error": SIMPLE_CONFIG,
            "test_attr_error": {
                "allow_methods": "__any__",
                "allow_models": "__all__",
                "reject_models": [],
            },
            "test_hide": {
                "allow_methods": ALL_METHODS,
                "allow_models": "__all__",
                "reject_models": [],
                "auth.Permission": {
                    "hidden_fields": {"codename": "********"},
                    "allow_methods": ALL_METHODS,
                },
            },
        }

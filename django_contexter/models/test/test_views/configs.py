from django_contexter.models.method_types import ALL_METHODS, ALL_SAFE_METHODS


class Configs:
    @property
    def configs(self):
        return {
            "test_call_with_modelName": {
                "allow_methods": ALL_SAFE_METHODS,
                "allow_models": "__all__",
                "reject_models": [],
            },
            "test_all_call": {
                "allow_methods": ALL_SAFE_METHODS,
                "allow_models": "__all__",
                "reject_models": [],
            },
            "test_get_call": {
                "allow_methods": ALL_SAFE_METHODS,
                "allow_models": "__all__",
                "reject_models": [],
            },
            "test_check_method": {
                "allow_methods": ALL_SAFE_METHODS,
                "allow_models": "__all__",
                "reject_models": [],
            },
            "test_field_error": {
                "allow_methods": ALL_SAFE_METHODS,
                "allow_models": "__all__",
                "reject_models": [],
            },
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
                    "hidden_fields": ["codename"],
                    "allow_methods": ALL_METHODS,
                },
            },
        }

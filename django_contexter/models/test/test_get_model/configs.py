from django_contexter.models.method_lists import ALL_METHODS, ALL_SAFE_METHODS

# ? Why need noqa: WPS226?
# * These are different variations of
# * the configuration whose string
# * literals cannot be fixed


class ConfigErrorsConfigs(object):
    """Configs for ModelConfigTestCase."""

    @property
    def configs(self):
        """
        Configs for ModelConfigTestCase.

        Returns:
            dict: Configs
        """
        return {
            "test_both_all": {
                "allow_methods": ALL_METHODS,
                "allow_models": "__all__",
                "reject_models": "__all__",
            },
            "test_controversial_model": {
                "allow_methods": ALL_METHODS,
                "allow_models": ["auth.Permission"],
                "reject_models": ["auth.Permission"],
                # ? The message about the rejected request will be earlier than the configuration error.
                # * Make sure you are using an allowed model.
                # * This is quite expected behavior and is not an error,
                # ! but only for this type of error
            },
            "test_all_and_remaining": {
                "allow_methods": ALL_METHODS,
                "allow_models": "__all__",
                "reject_models": "__remaining__",
            },
            "test_remaining_and_all": {
                "allow_methods": ALL_METHODS,
                "allow_models": "__remaining__",
                "reject_models": "__all__",
            },
            "test_both_remaining": {
                "allow_methods": ALL_METHODS,
                "allow_models": "__remaining__",
                "reject_models": "__remaining__",
                "auth.Permission": {},
            },
        }


class JustConfigs(object):
    """Configs for ConfigsTestCase."""

    @property
    def configs(self):
        """
        Configs for ConfigsTestCase.

        Returns:
            dict: Configs
        """
        return {
            "test_allow": {
                "allow_methods": ALL_METHODS,
                "allow_models": "__all__",
                "reject_models": [],
            },
            "test_reject": {
                "allow_methods": ALL_METHODS,
                "allow_models": "__remaining__",
                "reject_models": ["auth.User"],
            },
            "test_reject_all": {
                "allow_methods": ALL_METHODS,
                "allow_models": [],
                "reject_models": "__all__",
            },
            "test_reject_remaining": {
                "allow_methods": ALL_METHODS,
                "allow_models": ["auth.User"],
                "reject_models": "__remaining__",
            },
            "test_allow_undeclared": {
                "allow_methods": ALL_METHODS,
                "allow_models": "__undeclared__",
                "reject_models": "__remaining__",
                "auth.User": {},
            },
            "test_reject_undeclared": {
                "allow_methods": ALL_METHODS,
                "allow_models": "__remaining__",
                "reject_models": "__undeclared__",
                "auth.User": {},
            },
            "test_emty_props": {
                "allow_methods": ALL_METHODS,
                "allow_models": "__remaining__",
                "reject_models": "__undeclared__",
                "auth.Permission": {"testProps": True},
            },
        }


class MethodsConfigs(object):
    """Configs for MethodsTestCase."""

    @property
    def configs(self):
        """
        Configs for MethodsTestCase.

        Returns:
            dict: Configs
        """
        return {
            "test_local_reject_method": {
                "allow_methods": [],
                "allow_models": "__remaining__",
                "reject_models": "__undeclared__",
                "auth.Permission": {
                    "allow_methods": ALL_SAFE_METHODS,
                },
            },
            "test_global_reject_method": {
                "allow_methods": ALL_SAFE_METHODS,
                "allow_models": "__all__",
                "reject_models": [],
            },
            "test_local_any": {
                "allow_methods": [],
                "allow_models": "__remaining__",
                "reject_models": "__undeclared__",
                "auth.Permission": {
                    "allow_methods": "__any__",
                },
            },
        }

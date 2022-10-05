from django_contexter.models.method_types import ALL_METHODS, ALL_SAFE_METHODS


class Config_errors_Configs:
    @property
    def configs(self):
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
                #! but only for this type of error
            },
            "test_all_and_remaining": {
                "allow_methods": ALL_METHODS,
                "allow_models": "__all__",
                "reject_models": "__remaining__",
            },
            "test_both_remaining": {
                "allow_methods": ALL_METHODS,
                "allow_models": "__remaining__",
                "reject_models": "__remaining__",
                "auth.Permission": {},
            },
        }


class Just_Configs:
    @property
    def configs(self):
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


class Methods_Configs:
    @property
    def configs(self):
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
            # "test_any": {
            #     "allow_methods": "__any__",
            #     "allow_models": "__all__",
            #     "reject_models": [],
            # }
        }


class Errors_Config:
    @staticmethod
    def config():
        return {
            "allow_methods": ALL_SAFE_METHODS,
            "allow_models": ["model_NotExists", "model.NotExists"],
            "reject_models": [],
        }

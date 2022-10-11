from django_contexter.models.errors.configuration_error import ConfigurationError


class Configuration(object):
    """Part of get_model.py: Contains ConfigurationError checks."""

    # TODO: Use own __init__
    def _all_at_the_same_time(self):
        if self.allowed_models == "__all__" and self.rejected_models == "__all__":
            raise ConfigurationError("".join([
                "allow_models and reject_models",
                "can't be __all__ at the same time",
            ]))

    def _allowed_and_rejected_at_the_same_time(self):
        if self.modelName in self.rejected_models and self.modelName in self.allowed_models:
            raise ConfigurationError("".join([
                "The same model can't be in rejected_models",
                "and allowed_models at the same time",
            ]))

    def _all_and_remaining_at_the_same_time(self):
        err = ConfigurationError("Using __all__ with __remaining__ will not work")

        if self.allowed_models == "__all__" and self.rejected_models == "__remaining__":
            raise err
        elif self.rejected_models == "__all__" and self.allowed_models == "__remaining__":
            raise err

    def _both_remaining(self):
        if self.allowed_models == "__remaining__" and self.rejected_models == "__remaining__":
            raise ConfigurationError("Using both __remaining__ will not work")

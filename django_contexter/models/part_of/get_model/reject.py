import django
from django.conf import settings

from django_contexter.models.errors.reject_error import RejectError

# ? Why need noqa: WPS437?
# * Because Django doesn't forbid the use of _meta
# https://docs.djangoproject.com/en/4.1/ref/models/meta/


class Reject(object):
    """Part of get_model.py: Contains RejectError checks."""

    def _model_rejected(self):
        self._apply_aliases()

        err = RejectError("This model is not allowed for use", self.modelName)

        if self.modelName in self.rejected_models:
            raise err
        elif self.modelName not in self.allowed_models:
            raise err

    def _apply_aliases(self):
        models = django.apps.apps.get_models(
            include_auto_created=True,
            include_swapped=True,
        )
        labels = [model._meta.label for model in models]

        if self.rejected_models == "__all__":
            self.rejected_models = labels
        elif self.rejected_models == "__undeclared__":
            self.rejected_models = set(labels) - set(settings.CONTEXTER_ACCESS_POLICY)

        if self.allowed_models == "__all__":
            self.allowed_models = labels
        elif self.allowed_models == "__undeclared__":
            self.allowed_models = set(labels) - set(settings.CONTEXTER_ACCESS_POLICY)

        if self.rejected_models == "__remaining__":
            self.rejected_models = set(labels) - set(self.allowed_models)
        elif self.allowed_models == "__remaining__":
            self.allowed_models = set(labels) - set(self.rejected_models)

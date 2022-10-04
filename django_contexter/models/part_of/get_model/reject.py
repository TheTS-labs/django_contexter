from django.conf import settings

import django

from ...errors.reject_error import RejectError

import time


class Reject:
    def _model_rejected(self):
        self.__apply_alias()

        if (
            self.modelName in self.rejected_models
            or self.modelName not in self.allowed_models
        ):
            raise RejectError("This model is not allowed for use", self.modelName)

    def __apply_alias(self):
        models = django.apps.apps.get_models(
            include_auto_created=True, include_swapped=True
        )
        all = [m._meta.label for m in models]

        if self.rejected_models == "__all__":
            self.rejected_models = all
        if self.allowed_models == "__all__":
            self.allowed_models = all

        if self.allowed_models == "__remaining__":
            self.allowed_models = set(all) - set(self.rejected_models)

        if self.rejected_models == "__remaining__":
            self.rejected_models = set(all) - set(self.allowed_models)

        if self.rejected_models == "__uneclared__":
            self.rejected_models = set(all) - set(settings.CONTEXTER_ACCESS_POLICY)

        if self.allowed_models == "__uneclared__":
            self.allowed_models = set(all) - set(settings.CONTEXTER_ACCESS_POLICY)

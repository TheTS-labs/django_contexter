from django.conf import settings

from ...errors.reject_error import RejectError


class Reject:
    def _model_rejected(self):
        if self.modelName in self.rejected_models:
            raise RejectError("This model is not allowed for use", self.modelName)

    def _remaining_and_not_allowed(self):
        if (
            self.rejected_models == "__remaining__"
            and self.modelName not in self.allowed_models
        ):
            raise RejectError("This model is not listed as allowed", self.modelName)

    def _undeclared(self):
        if (
            self.rejected_models == "__undeclared__"
            and self.modelName not in settings.CONTEXTER_ACCESS_POLICY
        ):
            raise RejectError("This model is not listed as authorized", self.modelName)

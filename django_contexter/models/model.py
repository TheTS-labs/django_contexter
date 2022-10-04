import django
from django.conf import settings
from rest_framework import status

from django_contexter.models.errors.reject_error import RejectError

from .errors.err_codes import MODEL_DOES_NOT_EXIST
from .errors.request_error import RequestError
from .part_of.get_model.configuration import Configuration
from .part_of.get_model.reject import Reject


class Model(Configuration, Reject):
    def __init__(self, modelName):
        self.modelName = modelName
        self.allowed_models = settings.CONTEXTER_ACCESS_POLICY["allow_models"]
        self.rejected_models = settings.CONTEXTER_ACCESS_POLICY["reject_models"]

        self.check_models_policy()

    def check_method(self, method):
        if self.props is None or self.props == {}:
            if (
                method not in settings.CONTEXTER_ACCESS_POLICY["allow_methods"]
                and settings.CONTEXTER_ACCESS_POLICY["allow_methods"] != "__all__"
            ):
                raise RejectError("API Method not allowed", method)
        else:
            if (
                method not in self.props["allow_methods"]
                and self.props["allow_methods"] != "__all__"
            ):
                raise RejectError("API Method not allowed for this model", method)

        return True

    def get_model_by_path(self):
        try:
            return django.apps.apps.get_model(self.modelName)
        except (LookupError, ValueError):
            raise RequestError(
                f"There is no model named {self.modelName}",
                MODEL_DOES_NOT_EXIST,
                status.HTTP_400_BAD_REQUEST,
            )

    def check_models_policy(self):
        """Checks the Access Policy for the model"""
        self._all_at_the_same_time()
        self._allowed_and_rejected_at_the_same_time()
        self._all_and_remaining_at_the_same_time()

        # Warning! rejected_models are always a higher priority

        self._model_rejected()
        self._remaining_and_not_allowed()
        self._undeclared()

    @property
    def model(self):
        return self.get_model_by_path()

    @property
    def props(self):
        if self.modelName in settings.CONTEXTER_ACCESS_POLICY:
            return settings.CONTEXTER_ACCESS_POLICY[self.modelName]

        return None

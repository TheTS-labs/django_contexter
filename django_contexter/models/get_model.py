"""Module with GetModel class."""

import django
from django.conf import settings
from rest_framework import status

from django_contexter.models.errors.err_codes import MODEL_DOES_NOT_EXIST
from django_contexter.models.errors.reject_error import RejectError
from django_contexter.models.errors.request_error import RequestError
from django_contexter.models.part_of.get_model.configuration import Configuration
from django_contexter.models.part_of.get_model.reject import Reject


class GetModel(Configuration, Reject):
    """Get model by model name."""

    def __init__(self, model_name):
        """
        Save model name and check Access Policy.

        Args:
            model_name: Model name from request
        """  # TODO: Use super calls
        self.modelName = model_name
        self.allowed_models = settings.CONTEXTER_ACCESS_POLICY["allow_models"]
        self.rejected_models = settings.CONTEXTER_ACCESS_POLICY["reject_models"]

        self._check_models_policy()

    @property
    def model(self):
        """
        Return model instance.

        Returns:
            Model inctance
        """
        return self._get_model_by_path()

    @property
    def props(self):
        """
        Return model props or global props.

        Returns:
            Model inctance
        """  # TODO: Rename to access_policy
        if self.modelName in settings.CONTEXTER_ACCESS_POLICY:
            return settings.CONTEXTER_ACCESS_POLICY.get(self.modelName)

        return None

    def check_method(self, method):
        """
        Check method according to Access Policy.

        Sus.

        Args:
            method: Method string, e. g. "get", "filter"

        Raises:
            RejectError: If method is not allowed

        Returns:
            boolean: True if no errors
        """
        if not self.props:
            self._check_method_globally(method)
        elif method not in self.props["allow_methods"]:
            if self.props["allow_methods"] != "__any__":
                raise RejectError("API Method not allowed for this model", method)

        return True

    def _check_method_globally(self, method):
        if method not in settings.CONTEXTER_ACCESS_POLICY["allow_methods"]:
            if settings.CONTEXTER_ACCESS_POLICY["allow_methods"] != "__any__":
                raise RejectError("API Method not allowed", method)

    def _check_models_policy(self):
        """Check the Access Policy for the model."""
        self._all_at_the_same_time()
        self._allowed_and_rejected_at_the_same_time()
        self._all_and_remaining_at_the_same_time()
        self._both_remaining()

        # Warning! rejected_models are always a higher priority

        self._model_rejected()

    def _get_model_by_path(self):
        try:
            return django.apps.apps.get_model(self.modelName)
        except (LookupError, ValueError):
            raise RequestError(
                f"There is no model named {self.modelName}",
                MODEL_DOES_NOT_EXIST,
                status.HTTP_400_BAD_REQUEST,
            )

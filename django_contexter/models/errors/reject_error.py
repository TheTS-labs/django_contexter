from rest_framework.status import HTTP_403_FORBIDDEN

from django_contexter.models.errors.err_codes import REJECT_ERROR
from django_contexter.models.errors.request_error import RequestError


class RejectError(RequestError):
    """Exception raised if request rejected."""

    def __init__(
        self,
        reject_reason="Unknown Reason",
        reject_object="Unknown Model",
    ):
        """
        Save reject_reason and reject_object of error.

        Args:
            reject_object: (string) Name of reject object
            reject_reason: Reason of reject
        """
        self.err_code = REJECT_ERROR
        self.message = f"Request was rejected({reject_object}). Reason: {reject_reason}"
        self.status = HTTP_403_FORBIDDEN
        super().__init__(self.message, self.err_code, self.status)

from rest_framework.status import HTTP_500_INTERNAL_SERVER_ERROR

from django_contexter.models.errors.err_codes import SERVER_WRONG_CONFIG
from django_contexter.models.errors.request_error import RequestError


class ConfigurationError(RequestError):
    """Exception raised if configuration wrong."""

    def __init__(self, message):
        """
        Save message of error.

        Args:
            message: Error message
        """
        self.err_code = SERVER_WRONG_CONFIG
        self.message = message
        self.status = HTTP_500_INTERNAL_SERVER_ERROR
        super().__init__(self.message, self.err_code, self.status)

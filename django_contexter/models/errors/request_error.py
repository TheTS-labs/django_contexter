from rest_framework.response import Response
from rest_framework.status import HTTP_500_INTERNAL_SERVER_ERROR


class RequestError(Exception):
    """Exception raised for errors in the request.

    Attributes:
        message -- Message that containse error reason
        err_code -- Iternal API error code
        status -- HTTP status code
    """

    def __init__(
        self,
        message="Unknown Error",
        err_code=-1,
        status=HTTP_500_INTERNAL_SERVER_ERROR,
    ):
        self.err_code = err_code
        self.message = message
        self.status = status
        super().__init__(self.message)

    @property
    def response(self):
        """Return Response object with err_code, err_msg and status code"""
        return Response(
            {"err_code": self.err_code, "err_msg": self.message}, status=self.status
        )

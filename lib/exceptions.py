from rest_framework.exceptions import (
    APIException,
    AuthenticationFailed,
    PermissionDenied,
)
from rest_framework.response import Response
from rest_framework.views import exception_handler


class CustomAPIException(APIException):
    def __init__(self, error_code, error_message, status_code=400, details=None):
        self.error_code = error_code
        self.error_message = error_message
        self.details = details
        self.status_code = status_code

        super().__init__(error_message)


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        error_code = "UNKNOWN_ERROR"
        error_message = "Unknown error"
        details = None

        if isinstance(exc, AuthenticationFailed):
            error_code = "AUTHENTICATION_FAILED"
            error_message = exc.detail
            response.data = {
                "error_code": error_code,
                "error_message": error_message,
                "details": details,
            }

        if isinstance(exc, CustomAPIException):
            error_code = exc.error_code
            error_message = exc.error_message
            details = exc.details

            response.data = {
                "error_code": error_code,
                "error_message": error_message,
                "details": details,
            }

    return response

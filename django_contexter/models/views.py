"""Use API logic and return response."""

import json

from django.core.exceptions import FieldError, ObjectDoesNotExist
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from django_contexter.models.change_result import ChangeResult
from django_contexter.models.errors.configuration_error import ConfigurationError
from django_contexter.models.errors.err_codes import (
    FIELD_ERROR,
    FUNCTION_DOES_NOT_EXIST_IN_QUERYSET_API,
    NO_MANDATORY_PARAMETER_MODELNAME,
)
from django_contexter.models.errors.reject_error import RejectError
from django_contexter.models.errors.request_error import RequestError
from django_contexter.models.model import Model
from django_contexter.models.serializer import Serializer


def error_handler(func):
    """
    Handle RequestError, RejectError and ConfigurationError and send Response.

    Args:
        func: The decorator function

    Returns:
        rest_framework.response.Response
            Response with error or request request_result
    """

    def inner_function(*args, **kwargs):  # noqa: WPS430
        try:
            return func(*args, **kwargs)
        except (RequestError, RejectError, ConfigurationError) as err:
            return err.response

    return inner_function


def exclude_keys(dictionary, keys):
    """
    Exclude keys from dict.

    https://stackoverflow.com/a/31434038/19729483

    Args:
        dictionary: The dict to work with
        keys: The keys to exclude

    Returns:
        dict: dict after excluding keys
    """
    return {key: dictionary[key] for key in dictionary if key not in keys}


def _check_modelname_in_request(request_get):
    if "modelName" not in request_get:
        raise RequestError(
            "modelName is a required parameter",
            NO_MANDATORY_PARAMETER_MODELNAME,
            status.HTTP_400_BAD_REQUEST,
        )


def _get_model_request(get_parameter):
    try:
        model_request = json.loads(get_parameter)
    except json.JSONDecodeError:
        model_request = {}

    return model_request


@api_view(["GET"])
@error_handler
def index(request):
    """
    Return model records by GET parameters.

    Args:
        request: Django request object

    Returns:
        rest_framework.response.Response: Response with request result

    Raises:
        RequestError: If Request is invalid
    """
    _check_modelname_in_request(request.GET)

    model = Model(request.GET.get("modelName"))
    changer = ChangeResult(model.props, model.model, request)

    request_result = model.model.objects

    for key in exclude_keys(request.GET, ["modelName"]):
        model_request = {
            "request": _get_model_request(request.GET.get(key)),
            "function_name": "".join(filter(lambda letter: not letter.isdigit(), key)),
        }

        model.check_method(model_request["function_name"])

        try:
            model_request.update(
                {"function": getattr(request_result, model_request["function_name"])}
            )
        except AttributeError as exc:
            raise RequestError(
                f"No function named '{model_request['function_name']}' in QuerySet API",
                FUNCTION_DOES_NOT_EXIST_IN_QUERYSET_API,
                status.HTTP_400_BAD_REQUEST,
            ) from exc

        try:
            request_result = model_request["function"](**model_request["request"])
        except (FieldError, ObjectDoesNotExist) as err:
            raise RequestError(
                err.args[0],
                FIELD_ERROR,
                status.HTTP_400_BAD_REQUEST,
            ) from err

    return Response(
        Serializer(
            instance=changer.fix_fields(request_result),
            many=not isinstance(request_result, model.model),
            context={
                "model": model.model,
                "fields": "__all__",
            },
        ).data,
    )

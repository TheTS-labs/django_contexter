import json

from django.core.exceptions import FieldError, ObjectDoesNotExist
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .change_result import ChangeResult
from .errors.configuration_error import ConfigurationError
from .errors.err_codes import (
    FIELD_ERROR,
    FUNCTION_DOES_NOT_EXIST_IN_QUERYSET_API,
    NO_MANDATORY_PARAMETER_MODELNAME,
)
from .errors.reject_error import RejectError
from .errors.request_error import RequestError
from .get_model import GetModel
from .serializer import Serializer


def Error_Handler(func):
    """Handle AssertionError and FieldError in view and send as Response"""

    def Inner_Function(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (RequestError, RejectError, ConfigurationError) as err:
            return err.response

    return Inner_Function


def exclude_keys(dictionary, keys):
    """https://stackoverflow.com/a/31434038/19729483"""

    return {x: dictionary[x] for x in dictionary if x not in keys}


@api_view(["GET"])
@Error_Handler
def index(request):
    """Return model records by GET parameters"""
    if "modelName" not in request.GET:
        raise RequestError(
            "modelName is a required parameter",
            NO_MANDATORY_PARAMETER_MODELNAME,
            status.HTTP_400_BAD_REQUEST,
        )

    gm = GetModel(request.GET.get("modelName"))
    model = gm.model
    changer = ChangeResult(gm.props, model, request)

    result = model.objects

    for key in exclude_keys(request.GET, ["modelName"]):
        try:
            model_request = json.loads(request.GET.get(key))
        except json.JSONDecodeError:
            model_request = {}

        try:
            request_function_name = "".join(filter(lambda x: not x.isdigit(), key))
            gm.check_method(request_function_name)
            request_function = getattr(result, request_function_name)
            result = request_function(**model_request)
        except AttributeError as exc:
            raise RequestError(
                f"No function named '{request_function_name}' in QuerySet API",
                FUNCTION_DOES_NOT_EXIST_IN_QUERYSET_API,
                status.HTTP_400_BAD_REQUEST,
            ) from exc
        except (FieldError, ObjectDoesNotExist) as err:
            raise RequestError(
                err.args[0], FIELD_ERROR, status.HTTP_400_BAD_REQUEST
            ) from err

    result = changer.fix_fields(result)

    return Response(
        Serializer(
            instance=result,
            many=not isinstance(result, model),
            context={
                "model": model,
                "fields": "__all__",
            },
        ).data
    )

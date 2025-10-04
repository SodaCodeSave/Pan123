import json

from typing import Any, Type
from requests import Response, HTTPError
from .exceptions import CloudError


def parse_response_data(
    response: Response,
    fail_raise: Type[Exception] = CloudError,
) -> Any:
    if response.status_code == 200:
        response_data = json.loads(response.text)
        if response_data["code"] == 0:
            return response_data["data"]
        else:
            raise fail_raise(response_data)
    else:
        raise HTTPError(response.text)

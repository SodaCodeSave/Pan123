import json
import requests

from typing import Union
from .utils.exceptions import ClientKeyError
from .utils.dict_util import merge_dict
from .utils.request import parse_response_data


def get_access_token(
    client_id: str,
    client_secret: str,
    base_url: str = "https://open-api.123pan.com",
    header: Union[dict, None] = None,
) -> str:
    header = header or {"Content-Type": "application/json", "Platform": "open_platform"}
    url = base_url + "/api/v1/access_token"
    data = {"clientID": client_id, "clientSecret": client_secret}
    response = requests.post(url, data=data, headers=header)
    return parse_response_data(response, ClientKeyError)["accessToken"]

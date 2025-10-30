import requests

from .utils.exceptions import ClientKeyError
from .utils.request import parse_response_data
from .abstracts import Requestable


class Auth(Requestable):
    def get_access_token(
        self,
        client_id: str,
        client_secret: str,
    ) -> str:
        return parse_response_data(
            requests.post(
                self.use_url("/api/v1/access_token"),
                data={"clientID": client_id, "clientSecret": client_secret},
                headers=self.header,
            ),
            ClientKeyError,
        )["accessToken"]
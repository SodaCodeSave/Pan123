import requests

from .utils.request import parse_response_data
from .abstracts import Requestable


class User(Requestable):
    def info(self) -> dict:
        return parse_response_data(
            requests.get(
                self.use_url("/api/v1/user/info"),
                headers=self.header,
            )
        )

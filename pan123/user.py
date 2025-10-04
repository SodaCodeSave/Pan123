import requests

from .utils import check_status_code


class User:
    header: dict
    base_url: str

    def __init__(self, base_url, header):
        self.header = header
        self.base_url = base_url

    def info(self):
        url = self.base_url + "/api/v1/user/info"
        r = requests.get(url, headers=self.header)
        return check_status_code(r)

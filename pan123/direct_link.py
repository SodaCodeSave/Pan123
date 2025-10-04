import requests

from .utils.request import parse_response_data
from .abstracts import Requestable


class DirectLink(Requestable):
    def doPost(self, url: str, data: dict):
        return parse_response_data(
            requests.post(
                self.use_url(f"/api/v1/direct-link/{url}"),
                data=data,
                headers=self.header,
            )
        )

    def query_transcode(self, ids: list):
        return self.doPost("queryTranscode", {"ids": ids})

    def do_transcode(self, ids):
        return self.doPost("doTranscode", {"ids": ids})

    def get_m3u8(self, file_id):
        return self.doPost("get/m3u8", {"fileID": file_id})

    def enable(self, file_id):
        return self.doPost("enable", {"fileID": file_id})

    def disable(self, file_id):
        return self.doPost("disable", {"fileID": file_id})

    def list_url(self, file_id):
        return self.doPost("url", {"fileID": file_id})

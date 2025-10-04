import requests

from .utils.request import parse_response_data
from .abstracts import Requestable


class OfflineDownload(Requestable):
    def download(
        self,
        download_url: str,
        file_name: str = "",
        save_path: str = "",
        call_back_url: str = "",
    ):
        data = {"url": download_url}
        if file_name:
            data["fileName"] = file_name
        if save_path:
            data["savePath"] = save_path
        if call_back_url:
            data["callBackUrl"] = call_back_url
        return parse_response_data(
            requests.post(
                self.use_url("/api/v1/offline/download"),
                data=data,
                headers=self.header,
            )
        )

    def download_process(self, task_id):
        return parse_response_data(
            requests.post(
                self.use_url("/api/v1/offline/download/process"),
                data={"taskID": task_id},
                headers=self.header,
            )
        )

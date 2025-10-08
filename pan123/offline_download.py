import requests

from .utils import check_status_code, is_valid_url, UrlError


class OfflineDownload:
    def __init__(self, base_url, header):
        self.header = header
        self.base_url = base_url

    def download(self, download_url, file_name=None, save_path=None, call_back_url=None):
        url = self.base_url + "/api/v1/offline/download"
        if not is_valid_url(download_url):
            raise UrlError(download_url)
        data = {
            "url": download_url
        }
        if file_name:
            data["fileName"] = file_name
        if save_path:
            data["savePath"] = save_path
        if call_back_url:
            data["callBackUrl"] = call_back_url
        r = requests.post(url, data=data, headers=self.header)
        return check_status_code(r)

    def download_process(self, task_id):
        url = self.base_url + "/api/v1/offline/download/process"
        data = {
            "taskID": task_id
        }
        r = requests.post(url, data=data, headers=self.header)
        return check_status_code(r)

import requests

from .utils import check_status_code


class DirectLink:
    def __init__(self, base_url, header):
        self.header = header
        self.base_url = base_url

    def query_transcode(self, ids):
        url = self.base_url + "/api/v1/direct-link/queryTranscode"
        data = {
            "ids": ids
        }
        r = requests.post(url, data=data, headers=self.header)
        return check_status_code(r)

    def do_transcode(self, ids):
        url = self.base_url + "/api/v1/direct-link/doTranscode"
        data = {
            "ids": ids,
        }
        r = requests.post(url, data=data, headers=self.header)
        return check_status_code(r)

    def get_m3u8(self, file_id):
        url = self.base_url + "/api/v1/direct-link/get/m3u8"
        data = {
            "fileID": file_id,
        }
        r = requests.post(url, data=data, headers=self.header)
        return check_status_code(r)

    def enable(self, file_id):
        url = self.base_url + "/api/v1/direct-link/enable"
        data = {
            "fileID": file_id,
        }
        r = requests.post(url, data=data, headers=self.header)
        return check_status_code(r)

    def disable(self, file_id):
        url = self.base_url + "/api/v1/direct-link/disable"
        data = {
            "fileID": file_id,
        }
        r = requests.post(url, data=data, headers=self.header)
        return check_status_code(r)

    def list_url(self, file_id):
        url = self.base_url + "/api/v1/direct-link/url"
        data = {
            "fileID": file_id,
        }
        r = requests.post(url, data=data, headers=self.header)
        return check_status_code(r)

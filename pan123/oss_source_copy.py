import requests

from .utils import check_status_code


class OSSSourceCopy:
    def __init__(self, base_url, header):
        self.header = header
        self.base_url = base_url

    def copy(self, file_ids, to_parent_file_id):
        url = self.base_url + "/api/v1/oss/source/copy"
        data = {
            "fileIDs": file_ids,
            "toParentFileID": to_parent_file_id,
            "sourceType": 1,
            "type": 1
        }
        r = requests.post(url, data=data, headers=self.header)
        return check_status_code(r)

    def fail(self, task_id, limit, page):
        url = self.base_url + "/api/v1/oss/source/copy/fail"
        data = {
            "taskID": task_id,
            "limit": limit,
            "page": page
        }
        r = requests.post(url, data=data, headers=self.header)
        return check_status_code(r)

    def process(self, task_id):
        url = self.base_url + "/api/v1/oss/source/copy/process"
        data = {
            "taskID": task_id
        }
        r = requests.post(url, data=data, headers=self.header)
        return check_status_code(r)

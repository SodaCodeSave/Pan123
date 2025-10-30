import requests

from .utils.request import parse_response_data
from .abstracts import Requestable


class OSSSourceCopy(Requestable):
    def copy(self, file_ids: list[int], to_parent_file_id: int):
        return parse_response_data(
            requests.post(
                self.use_url("/api/v1/oss/source/copy"),
                data={
                    "fileIDs": file_ids,
                    "toParentFileID": to_parent_file_id,
                    "sourceType": 1,
                    "type": 1,
                },
                headers=self.header,
            )
        )

    def fail(self, task_id: str, limit: int = 1, page: int = 0):
        return parse_response_data(
            requests.post(
                self.use_url("/api/v1/oss/source/copy/fail"),
                data={
                    "taskID": task_id,
                    "limit": limit,
                    "page": page,
                },
                headers=self.header,
            )
        )

    def process(self, task_id: str):
        return parse_response_data(
            requests.post(
                self.use_url("/api/v1/oss/source/copy/process"),
                data={"taskID": task_id},
                headers=self.header,
            )
        )

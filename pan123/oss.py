import hashlib, requests, os, math

from .utils.request import parse_response_data
from .utils.file_metadata import get_file_md5
from .utils.exceptions import PacketLossError
from .abstracts import Requestable
from .oss_source_copy import OSSSourceCopy
from .costants import DuplicateMode


class OSS(Requestable):
    def __init__(self, base_url, header):
        super().__init__(base_url, header)
        self.source_copy = OSSSourceCopy(base_url, header)

    def list_file(
        self,
        parent_file_id: int,
        limit: int = 0,
        start_time: int = 0,
        end_time: int = 0,
        last_file_id: int = 0,
    ) -> dict:
        data = {
            "parentFileId": parent_file_id,
            "type": 1,
        }
        if limit:
            data["limit"] = limit
        if start_time:
            data["startTime"] = start_time
        if end_time:
            data["endTime"] = end_time
        if last_file_id:
            data["lastFileId"] = last_file_id
        return parse_response_data(
            requests.get(
                self.use_url("/api/v1/oss/file/list"),
                data=data,
                headers=self.header,
            )
        )

    def mkdir(self, name: str, parent_id: int):
        return parse_response_data(
            requests.get(
                self.use_url("/upload/v1/oss/file/mkdir"),
                data={
                    "name": name,
                    "parentID": parent_id,
                    "type": 1,
                },
                headers=self.header,
            )
        )

    def create(
        self,
        preupload_id: int,
        filename: str,
        etag: str,
        size: int,
        duplicate: DuplicateMode = DuplicateMode.RENAME,
    ):
        data = {
            "parentFileID": preupload_id,
            "filename": filename,
            "etag": etag,
            "size": size,
            "type": 1,
        }
        if duplicate:
            data["duplicate"] = duplicate
        return parse_response_data(
            requests.post(
                self.use_url("/upload/v1/oss/file/create"),
                data=data,
                headers=self.header,
            )
        )

    def get_upload_url(self, preupload_id: str, slice_index: int):
        return parse_response_data(
            requests.post(
                self.use_url("/upload/v1/oss/file/get_upload_url"),
                data={"preuploadID": preupload_id, "sliceNo": slice_index},
                headers=self.header,
            )
        )["presignedURL"]

    def list_upload_parts(self, preupload_id: str) -> list[dict]:
        return parse_response_data(
            requests.post(
                self.use_url("/upload/v1/oss/file/list_upload_parts"),
                data={"preuploadID": preupload_id},
                headers=self.header,
            )
        )

    def upload_complete(self, preupload_id: str):
        return parse_response_data(
            requests.post(
                self.use_url("/upload/v1/oss/file/upload_complete"),
                data={"preuploadID": preupload_id},
                headers=self.header,
            )
        )

    def upload_async_result(self, preupload_id: str):
        return parse_response_data(
            requests.post(
                self.use_url("/upload/v1/oss/file/upload_async_result"),
                data={"preuploadID": preupload_id},
                headers=self.header,
            )
        )

    def upload(self, preupload_id: int, file_path: str):
        upload_data_parts = {}
        f = self.create(
            preupload_id,
            os.path.basename(file_path),
            get_file_md5(file_path),
            os.stat(file_path).st_size,
        )
        num_slices = math.ceil(os.stat(file_path).st_size / f["sliceSize"])
        with open(file_path, "rb") as fi:
            for part in range(1, num_slices + 1):
                url = self.get_upload_url(f["preuploadID"], part)
                chunk = fi.read(f["sliceSize"])
                md5 = hashlib.md5(chunk).hexdigest()
                requests.put(url, data=chunk)
                upload_data_parts[part] = {
                    "md5": md5,
                    "size": len(chunk),
                }
        if not os.stat(file_path).st_size <= f["sliceSize"]:
            parts = self.list_upload_parts(f["preuploadID"])
            for part in parts:
                if not (
                    upload_data_parts[part]["md5"] == part["etag"]
                    and upload_data_parts[part]["size"] == part["size"]
                ):
                    raise PacketLossError(part["partNumber"])
        self.upload_complete(f["preuploadID"])

    def move(self, file_id_list: list[int], to_parent_file_id: int):
        return parse_response_data(
            requests.post(
                self.use_url("/api/v1/oss/file/move"),
                data={
                    "fileIDs": file_id_list,
                    "toParentFileID": to_parent_file_id,
                },
                headers=self.header,
            )
        )

    def delete(self, file_ids: list[int]):
        return parse_response_data(
            requests.post(
                self.use_url("/api/v1/oss/file/delete"),
                data={"fileIDs": file_ids},
                headers=self.header,
            )
        )

    def detail(self, file_id: int):
        r = requests.post(
            self.use_url("/api/v1/oss/file/detail"),
            data={"fileID": file_id},
            headers=self.header,
        )
        data = parse_response_data(r)
        data["trashed"] = bool(data["trashed"])
        data["type"] = not data["type"]
        return data

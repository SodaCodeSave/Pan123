import hashlib, requests, os, math

from .utils.exceptions import PacketLossError
from .utils.request import parse_response_data
from .utils.file_metadata import get_file_md5
from .abstracts import Requestable
from .costants import SearchMode, DuplicateMode
from typing import Literal


class File(Requestable):
    def legacy_list_file(
        self,
        parent_file_id: int,
        page: int = 0,
        limit: int = 0,
        order_by: str = "file_id",
        order_direction: Literal["asc", "desc"] = "asc",
        trashed: bool = False,
        search_data: str = "",
    ) -> list[dict]:
        data: dict = {"parentFileId": parent_file_id}
        if page:
            data["page"] = page
        if limit:
            data["limit"] = limit
        if order_by:
            data["orderBy"] = order_by
        if order_direction:
            data["orderDirection"] = order_direction
        if trashed:
            data["trashed"] = trashed
        if search_data:
            data["searchData"] = search_data
        return parse_response_data(
            requests.get(
                self.use_url("/api/v1/file/list"),
                data=data,
                headers=self.header,
            )
        )

    def list_file(
        self,
        parent_file_id: int,
        limit: int,
        search_data: str = "",
        search_mode: SearchMode.value = SearchMode.NORMAL.value,
        last_file_id: int = 0,
    ):
        data: dict = {"parentFileId": parent_file_id, "limit": limit}
        if search_data:
            data["searchData"] = search_data
        if search_mode:
            data["searchMode"] = search_mode
        if last_file_id:
            data["lastFileID"] = last_file_id
        return parse_response_data(
            requests.get(
                self.use_url("/api/v2/file/list"),
                data=data,
                headers=self.header,
            )
        )

    def mkdir(self, name: str, parent_id: int):
        return parse_response_data(
            requests.get(
                self.use_url("/upload/v1/file/mkdir"),
                data={"name": name, "parentID": parent_id},
                headers=self.header,
            )
        )

    def create(
        self,
        parent_file_id: int,
        filename: str,
        etag: str,
        size: int,
        duplicate: DuplicateMode = DuplicateMode.RENAME,
    ):
        data = {
            "parentFileID": parent_file_id,
            "filename": filename,
            "etag": etag,
            "size": size,
        }
        if duplicate:
            data["duplicate"] = duplicate.value
        return parse_response_data(
            requests.post(
                self.use_url("/upload/v1/file/create"),
                data=data,
                headers=self.header,
            )
        )

    def get_upload_url(self, preupload_id: str, slice_no: int) -> str:
        return parse_response_data(
            requests.post(
                self.use_url("/upload/v1/file/get_upload_url"),
                data={"preuploadID": preupload_id, "sliceNo": slice_no},
                headers=self.header,
            )
        )["presignedURL"]

    def list_upload_parts(self, preupload_id: str):
        return parse_response_data(
            requests.post(
                self.use_url("/upload/v1/file/list_upload_parts"),
                data={"preuploadID": preupload_id},
                headers=self.header,
            )
        )

    def upload_complete(self, preupload_id: str):
        return parse_response_data(
            requests.post(
                self.use_url("/upload/v1/file/upload_complete"),
                data={"preuploadID": preupload_id},
                headers=self.header,
            )
        )

    def upload_async_result(self, preupload_id: str):
        return parse_response_data(
            requests.post(
                self.use_url("/upload/v1/file/upload_async_result"),
                data={"preuploadID": preupload_id},
                headers=self.header,
            )
        )

    def upload(self, parent_file_id: int, file_path: str):
        upload_data_parts = {}
        file_metadata = self.create(
            parent_file_id,
            os.path.basename(file_path),
            get_file_md5(file_path),
            os.stat(file_path).st_size,
        )
        if file_metadata["reuse"]:
            return
        num_slices = math.ceil(os.stat(file_path).st_size / file_metadata["sliceSize"])
        with open(file_path, "rb") as file_stream:
            for i in range(1, num_slices + 1):
                url = self.get_upload_url(file_metadata["preuploadID"], i)
                chunk = file_stream.read(file_metadata["sliceSize"])
                md5 = hashlib.md5(chunk).hexdigest()
                requests.put(url, data=chunk)
                upload_data_parts[i] = {
                    "md5": md5,
                    "size": len(chunk),
                }
        if not os.stat(file_path).st_size <= file_metadata["sliceSize"]:
            parts = self.list_upload_parts(file_metadata["preuploadID"])
            for i in parts["parts"]:
                part = i["partNumber"]
                if not (
                    upload_data_parts[int(part)]["md5"] == i["etag"]
                    and upload_data_parts[int(part)]["size"] == i["size"]
                ):
                    raise PacketLossError(i["partNumber"])
        self.upload_complete(file_metadata["preuploadID"])

    def rename(self, rename_dict: dict):
        rename_list = []
        for old_name in rename_dict.keys():
            new_name = rename_dict[old_name]
            rename_list.append(f"{old_name}|{new_name}")
        return parse_response_data(
            requests.post(
                self.use_url("/api/v1/file/rename"),
                data={"renameList": rename_list},
                headers=self.header,
            )
        )

    def move(self, file_id_list: list[int], to_parent_file_id: int):
        return parse_response_data(
            requests.post(
                self.use_url("/api/v1/file/move"),
                data={"fileIDs": file_id_list, "toParentFileID": to_parent_file_id},
                headers=self.header,
            )
        )

    def to_trashed(self, file_ids):
        return parse_response_data(
            requests.post(
                self.use_url("/api/v1/file/trash"),
                data={"fileIDs": file_ids},
                headers=self.header,
            )
        )

    def recover(self, file_ids):
        return parse_response_data(
            requests.post(
                self.use_url("/api/v1/file/recover"),
                data={"fileIDs": file_ids},
                headers=self.header,
            )
        )

    def delete(self, file_ids):
        return parse_response_data(
            requests.post(
                self.use_url("/api/v1/file/delete"),
                data={"fileIDs": file_ids},
                headers=self.header,
            )
        )

    def detail(self, file_id):
        data = parse_response_data(
            requests.get(
                self.use_url("/api/v1/file/detail"),
                data={"fileID": file_id},
                headers=self.header,
            )
        )
        data["trashed"] = bool(data["trashed"])
        data["type"] = not data["type"]
        return data

    def download(self, file_id):
        return parse_response_data(
            requests.get(
                self.use_url("/api/v1/file/download"),
                data={"fileID": file_id},
                headers=self.header,
            )
        )["downloadURL"]

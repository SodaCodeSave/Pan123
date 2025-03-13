import hashlib

import requests

from .utils import check_status_code, get_file_md5


class OSS:
    def __init__(self, base_url, header):
        self.header = header
        self.base_url = base_url
        from .oss_offline_download import OSSOfflineDownload
        self.offline_download = OSSOfflineDownload(base_url, header)
        from .oss_source_copy import OSSSourceCopy
        self.source_copy = OSSSourceCopy(base_url, header)

    def list(self, parent_file_id: int, limit=None, start_time=None, end_time=None, last_file_id=None):
        url = self.base_url + "/api/v1/oss/file/list"
        data = {
            "parentFileId": parent_file_id,
            "type": 1
        }

        if limit:
            data["limit"] = limit
        if start_time:
            data["startTime"] = start_time
        if end_time:
            data["endTime"] = end_time
        if last_file_id:
            data["lastFileId"] = last_file_id

        r = requests.get(url, data=data, headers=self.header)

        return check_status_code(r)

    def mkdir(self, name: str, parent_id: int):
        # 构造请求URL和参数
        url = self.base_url + "/upload/v1/oss/file/mkdir"
        data = {
            "name": name,
            "parentID": parent_id,
            "type": 1
        }

        # 发送GET请求
        r = requests.get(url, data=data, headers=self.header)

        # 将响应内容解析为JSON格式
        return check_status_code(r)

    def create(self, preupload_id: int, filename: str, etag: str, size: int, duplicate: int = None):
        # 构造请求URL
        url = self.base_url + "/upload/v1/oss/file/create"
        # 准备请求数据
        data = {
            "parentFileID": preupload_id,
            # 文件名
            "filename": filename,
            # 文件的etag
            "etag": etag,
            # 文件大小
            "size": size,
            "type": 1
        }
        # 如果传入了重复处理方式参数，则添加到请求数据中
        if duplicate:
            data["duplicate"] = duplicate
        # 发送POST请求
        r = requests.post(url, data=data, headers=self.header)
        # 将响应内容解析为JSON格式
        return check_status_code(r)

    def get_upload_url(self, preupload_id: str, slice_no: int):
        # 构造请求URL
        url = self.base_url + "/upload/v1/oss/file/get_upload_url"
        # 准备请求数据
        data = {
            "preuploadID": preupload_id,
            "sliceNo": slice_no
        }
        # 发送POST请求
        r = requests.post(url, data=data, headers=self.header)
        # 将响应内容解析为JSON格式
        return check_status_code(r)["presignedURL"]

    def list_upload_parts(self, preupload_id: str):
        # 构造请求URL
        url = self.base_url + "/upload/v1/oss/file/list_upload_parts"
        # 准备请求数据
        data = {
            "preuploadID": preupload_id
        }
        # 发送POST请求
        r = requests.post(url, data=data, headers=self.header)
        # 将响应内容解析为JSON格式
        return check_status_code(r)

    def upload_complete(self, preupload_id: str):
        # 构造请求URL
        url = self.base_url + "/upload/v1/oss/file/upload_complete"
        # 准备请求数据
        data = {
            "preuploadID": preupload_id
        }
        # 发送POST请求
        r = requests.post(url, data=data, headers=self.header)
        # 将响应内容解析为JSON格式
        return check_status_code(r)

    def upload_async_result(self, preupload_id: str):
        # 构造请求URL
        url = self.base_url + "/upload/v1/oss/file/upload_async_result"
        # 准备请求数据
        data = {
            "preuploadID": preupload_id
        }
        # 发送POST请求
        r = requests.post(url, data=data, headers=self.header)
        # 将响应内容解析为JSON格式
        return check_status_code(r)

    def upload(self, preupload_id, file_path):
        # 一键上传文件
        import os
        import math
        upload_data_parts = {}
        f = self.create(preupload_id, os.path.basename(file_path), get_file_md5(file_path),
                        os.stat(file_path).st_size)
        num_slices = math.ceil(os.stat(file_path).st_size / f["sliceSize"])
        with open(file_path, "rb") as fi:
            for i in range(1, num_slices + 1):
                url = self.get_upload_url(f["preuploadID"], i)
                chunk = fi.read(f["sliceSize"])
                md5 = hashlib.md5(chunk).hexdigest()
                # 发送Put请求
                requests.put(url, data=chunk)
                upload_data_parts[i] = {
                    "md5": md5,
                    "size": len(chunk),
                }
        if not os.stat(file_path).st_size <= f["sliceSize"]:
            parts = self.list_upload_parts(f["preuploadID"])
            for i in parts["parts"]:
                part = i["partNumber"]
                if upload_data_parts[i]["md5"] == part["etag"] and upload_data_parts[i]["size"] == part["size"]:
                    pass
                else:
                    raise requests.HTTPError
        self.upload_complete(f["preuploadID"])

    def move(self, file_id_list: list, to_parent_file_id: int):
        # 构造请求URL
        url = self.base_url + "/api/v1/oss/file/move"
        # 准备请求数据
        data = {
            "fileIDs": file_id_list,
            "toParentFileID": to_parent_file_id
        }
        # 发送POST请求
        r = requests.post(url, data=data, headers=self.header)
        return check_status_code(r)

    def delete(self, file_ids):
        url = self.base_url + "/api/v1/oss/file/delete"
        data = {
            "fileIDs": file_ids
        }
        r = requests.post(url, data=data, headers=self.header)
        return check_status_code(r)

    def detail(self, file_id):
        url = self.base_url + "/api/v1/oss/file/detail"
        data = {
            "fileID": file_id
        }
        r = requests.post(url, data=data, headers=self.header)
        data = check_status_code(r)
        if data["trashed"] == 1:
            data["trashed"] = True
        else:
            data["trashed"] = False
        if data["type"] == 1:
            data["type"] = "folder"
        else:
            data["type"] = "file"
        return data

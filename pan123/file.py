import hashlib

import requests

from .utils import check_status_code, get_file_md5


class File:
    def __init__(self, base_url, header):
        self.header = header
        self.base_url = base_url

    def v1_list(self, parent_file_id: int, page=None, limit=None, order_by=None, order_direction=None, trashed=None, search_data=None):
        url = self.base_url + "/api/v1/file/list"
        data = {
            "parentFileId": parent_file_id
        }

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

        r = requests.get(url, data=data, headers=self.header)

        return check_status_code(r)

    def list(self, parent_file_id: int, limit: int, search_data=None, search_mode=None, last_file_id=None):
        # 构造请求URL和参数
        url = self.base_url + "/api/v2/file/list"
        data = {
            "parentFileId": parent_file_id,
            "limit": limit
        }
        if search_data:
            data["searchData"] = search_data
        if search_mode:
            data["searchMode"] = search_mode
        if last_file_id:
            data["lastFileID"] = last_file_id

        # 发送GET请求
        r = requests.get(url, data=data, headers=self.header)

        # 将响应内容解析为JSON格式
        return check_status_code(r)

    def mkdir(self, name: str, parent_id: int):
        # 构造请求URL和参数
        url = self.base_url + "/upload/v1/file/mkdir"
        data = {
            "name": name,
            "parentID": parent_id
        }

        # 发送GET请求
        r = requests.get(url, data=data, headers=self.header)

        # 将响应内容解析为JSON格式
        return check_status_code(r)

    def create(self, parent_file_id: int, filename: str, etag: str, size: int, duplicate: int = None):
        # 构造请求URL
        url = self.base_url + "/upload/v1/file/create"
        # 准备请求数据
        data = {
            "parentFileID": parent_file_id,
            # 文件名
            "filename": filename,
            # 文件的etag
            "etag": etag,
            # 文件大小
            "size": size
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
        url = self.base_url + "/upload/v1/file/get_upload_url"
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
        url = self.base_url + "/upload/v1/file/list_upload_parts"
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
        url = self.base_url + "/upload/v1/file/upload_complete"
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
        url = self.base_url + "/upload/v1/file/upload_async_result"
        # 准备请求数据
        data = {
            "preuploadID": preupload_id
        }
        # 发送POST请求
        r = requests.post(url, data=data, headers=self.header)
        # 将响应内容解析为JSON格式
        return check_status_code(r)

    def upload(self, parent_file_id, file_path):
        # 一键上传文件
        import os
        import math
        upload_data_parts = {}
        f = self.create(parent_file_id, os.path.basename(file_path), get_file_md5(file_path),
                        os.stat(file_path).st_size)
        if f["reuse"]:
            return
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
                if upload_data_parts[int(part)]["md5"] == i["etag"] and upload_data_parts[int(part)]["size"] == i["size"]:
                    pass
                else:
                    raise requests.HTTPError
        self.upload_complete(f["preuploadID"])

    def rename(self, rename_dict: dict):
        # 构造请求URL
        url = self.base_url + "/api/v1/file/rename"
        # 准备请求数据
        rename_list = []
        for i in rename_dict.keys():
            rename_list.append(f"{i}|{rename_dict[i]}")
        data = {
            "renameList": rename_list
        }
        # 发送POST请求
        r = requests.post(url, data=data, headers=self.header)
        return check_status_code(r)

    def move(self, file_id_list: list, to_parent_file_id: int):
        # 构造请求URL
        url = self.base_url + "/api/v1/file/move"
        # 准备请求数据
        data = {
            "fileIDs": file_id_list,
            "toParentFileID": to_parent_file_id
        }
        # 发送POST请求
        r = requests.post(url, data=data, headers=self.header)
        return check_status_code(r)

    def trash(self, file_ids):
        url = self.base_url + "/api/v1/file/trash"
        data = {
            "fileIDs": file_ids
        }
        r = requests.post(url, data=data, headers=self.header)
        return check_status_code(r)

    def recover(self, file_ids):
        url = self.base_url + "/api/v1/file/recover"
        data = {
            "fileIDs": file_ids
        }
        r = requests.post(url, data=data, headers=self.header)
        return check_status_code(r)

    def delete(self, file_ids):
        url = self.base_url + "/api/v1/file/delete"
        data = {
            "fileIDs": file_ids
        }
        r = requests.post(url, data=data, headers=self.header)
        return check_status_code(r)

    def detail(self, file_id):
        url = self.base_url + "/api/v1/file/detail"
        data = {
            "fileID": file_id
        }
        r = requests.get(url, data=data, headers=self.header)
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

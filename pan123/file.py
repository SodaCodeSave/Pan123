import hashlib, requests, os, math

from .utils.exceptions import PacketLossError
from .utils.request import parse_response_data
from .utils.file_metadata import get_file_md5
from .abstracts import Requestable
from .costants import SearchMode, DuplicateMode
from typing import Literal


class File(Requestable):
    """文件管理类，提供文件相关的各种操作"""
    
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
        """
        获取文件列表（旧版接口）
        
        Args:
            parent_file_id: 父文件夹ID
            page: 页码
            limit: 每页数量
            order_by: 排序字段
            order_direction: 排序方向
            trashed: 是否获取回收站文件
            search_data: 搜索关键字
            
        Returns:
            文件列表
        """
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
        search_mode: SearchMode = SearchMode.NORMAL,
        last_file_id: int = 0,
    ):
        """
        获取文件列表（推荐版接口）
        
        Args:
            parent_file_id: 父文件夹ID
            limit: 每页数量
            search_data: 搜索关键字
            search_mode: 搜索模式
            last_file_id: 最后一个文件ID，用于分页
            
        Returns:
            文件列表
        """
        data: dict = {"parentFileId": parent_file_id, "limit": limit}
        if search_data:
            data["searchData"] = search_data
        if search_mode:
            data["searchMode"] = search_mode.value
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
        """
        创建目录
        
        Args:
            name: 目录名称
            parent_id: 父目录ID
            
        Returns:
            创建结果
        """
        return parse_response_data(
            requests.post(
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
        """
        创建文件（用于分片上传前的初始化）
        
        Args:
            parent_file_id: 父文件夹ID
            filename: 文件名
            etag: 文件的MD5值
            size: 文件大小
            duplicate: 重复文件处理方式
            
        Returns:
            创建结果，包含preuploadID等信息
        """
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
        """
        获取分片上传URL
        
        Args:
            preupload_id: 预上传ID
            slice_no: 分片序号
            
        Returns:
            预签名的分片上传URL
        """
        return parse_response_data(
            requests.post(
                self.use_url("/upload/v1/file/get_upload_url"),
                data={"preuploadID": preupload_id, "sliceNo": slice_no},
                headers=self.header,
            )
        )["presignedURL"]

    def list_upload_parts(self, preupload_id: str):
        """
        列举已上传的分片（非必需）
        
        Args:
            preupload_id: 预上传ID
            
        Returns:
            已上传分片列表
        """
        return parse_response_data(
            requests.post(
                self.use_url("/upload/v1/file/list_upload_parts"),
                data={"preuploadID": preupload_id},
                headers=self.header,
            )
        )

    def upload_complete(self, preupload_id: str):
        """
        上传完毕，通知服务器合并分片
        
        Args:
            preupload_id: 预上传ID
            
        Returns:
            上传完成结果
        """
        return parse_response_data(
            requests.post(
                self.use_url("/upload/v1/file/upload_complete"),
                data={"preuploadID": preupload_id},
                headers=self.header,
            )
        )

    def upload_async_result(self, preupload_id: str):
        """
        异步轮询获取上传结果
        
        Args:
            preupload_id: 预上传ID
            
        Returns:
            上传结果状态
        """
        return parse_response_data(
            requests.post(
                self.use_url("/upload/v1/file/upload_async_result"),
                data={"preuploadID": preupload_id},
                headers=self.header,
            )
        )

    def upload(self, parent_file_id: int, file_path: str):
        """
        完整文件上传流程
        
        Args:
            parent_file_id: 父文件夹ID
            file_path: 本地文件路径
            
        Raises:
            PacketLossError: 分片上传丢失或损坏时抛出
            
        Returns:
            无返回值，如果文件已存在且可复用则直接返回
        """
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
        """
        文件重命名
        
        Args:
            rename_dict: 重命名字典，键为旧文件名，值为新文件名
            
        Returns:
            重命名结果
        """
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
        """
        移动文件或文件夹
        
        Args:
            file_id_list: 要移动的文件/文件夹ID列表
            to_parent_file_id: 目标父文件夹ID
            
        Returns:
            移动结果
        """
        return parse_response_data(
            requests.post(
                self.use_url("/api/v1/file/move"),
                data={"fileIDs": file_id_list, "toParentFileID": to_parent_file_id},
                headers=self.header,
            )
        )

    def to_trashed(self, file_ids):
        """
        删除文件至回收站
        
        Args:
            file_ids: 要删除的文件/文件夹ID列表
            
        Returns:
            删除结果
        """
        return parse_response_data(
            requests.post(
                self.use_url("/api/v1/file/trash"),
                data={"fileIDs": file_ids},
                headers=self.header,
            )
        )

    def recover(self, file_ids):
        """
        从回收站恢复文件
        
        Args:
            file_ids: 要恢复的文件/文件夹ID列表
            
        Returns:
            恢复结果
        """
        return parse_response_data(
            requests.post(
                self.use_url("/api/v1/file/recover"),
                data={"fileIDs": file_ids},
                headers=self.header,
            )
        )

    def delete(self, file_ids):
        """
        彻底删除文件
        
        Args:
            file_ids: 要彻底删除的文件/文件夹ID列表
            
        Returns:
            删除结果
        """
        return parse_response_data(
            requests.post(
                self.use_url("/api/v1/file/delete"),
                data={"fileIDs": file_ids},
                headers=self.header,
            )
        )

    def detail(self, file_id):
        """
        获取单个文件详情
        
        Args:
            file_id: 文件ID
            
        Returns:
            文件详情信息，包含文件名、大小、类型、是否在回收站等
        """
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
        """
        获取文件下载链接
        
        Args:
            file_id: 文件ID
            
        Returns:
            文件的下载URL
        """
        return parse_response_data(
            requests.get(
                self.use_url("/api/v1/file/download"),
                data={"fileID": file_id},
                headers=self.header,
            )
        )

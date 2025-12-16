import hashlib, requests, os, math

from .utils.request import parse_response_data
from .utils.file_metadata import get_file_md5
from .utils.exceptions import PacketLossError
from .abstracts import Requestable
from .oss_source_copy import OSSSourceCopy
from .costants import DuplicateMode


class OSS(Requestable):
    """OSS存储管理类，提供OSS相关的各种操作"""
    
    def __init__(self, base_url, header):
        """
        初始化OSS管理类
        
        Args:
            base_url: API基础URL
            header: 请求头信息
        """
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
        """
        获取OSS文件列表
        
        Args:
            parent_file_id: 父文件夹ID
            limit: 每页数量
            start_time: 开始时间戳
            end_time: 结束时间戳
            last_file_id: 最后一个文件ID，用于分页
            
        Returns:
            OSS文件列表
        """
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
        """
        在OSS中创建目录
        
        Args:
            name: 目录名称
            parent_id: 父目录ID
            
        Returns:
            创建结果
        """
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
        """
        在OSS中创建文件（用于分片上传前的初始化）
        
        Args:
            preupload_id: 预上传ID
            filename: 文件名
            etag: 文件的MD5值
            size: 文件大小
            duplicate: 重复文件处理方式
            
        Returns:
            创建结果，包含preuploadID等信息
        """
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
        """
        获取OSS分片上传URL
        
        Args:
            preupload_id: 预上传ID
            slice_index: 分片序号
            
        Returns:
            预签名的分片上传URL
        """
        return parse_response_data(
            requests.post(
                self.use_url("/upload/v1/oss/file/get_upload_url"),
                data={"preuploadID": preupload_id, "sliceNo": slice_index},
                headers=self.header,
            )
        )["presignedURL"]

    def list_upload_parts(self, preupload_id: str) -> list[dict]:
        """
        列举OSS已上传的分片（非必需）
        
        Args:
            preupload_id: 预上传ID
            
        Returns:
            已上传分片列表
        """
        return parse_response_data(
            requests.post(
                self.use_url("/upload/v1/oss/file/list_upload_parts"),
                data={"preuploadID": preupload_id},
                headers=self.header,
            )
        )

    def upload_complete(self, preupload_id: str):
        """
        OSS上传完毕，通知服务器合并分片
        
        Args:
            preupload_id: 预上传ID
            
        Returns:
            上传完成结果
        """
        return parse_response_data(
            requests.post(
                self.use_url("/upload/v1/oss/file/upload_complete"),
                data={"preuploadID": preupload_id},
                headers=self.header,
            )
        )

    def upload_async_result(self, preupload_id: str):
        """
        OSS异步轮询获取上传结果
        
        Args:
            preupload_id: 预上传ID
            
        Returns:
            上传结果状态
        """
        return parse_response_data(
            requests.post(
                self.use_url("/upload/v1/oss/file/upload_async_result"),
                data={"preuploadID": preupload_id},
                headers=self.header,
            )
        )

    def upload(self, preupload_id: int, file_path: str):
        """
        OSS完整文件上传流程
        
        Args:
            preupload_id: 预上传ID
            file_path: 本地文件路径
            
        Raises:
            PacketLossError: 分片上传丢失或损坏时抛出
            
        Returns:
            无返回值
        """
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
        """
        移动OSS文件或文件夹
        
        Args:
            file_id_list: 要移动的文件/文件夹ID列表
            to_parent_file_id: 目标父文件夹ID
            
        Returns:
            移动结果
        """
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
        """
        删除OSS文件或文件夹
        
        Args:
            file_ids: 要删除的文件/文件夹ID列表
            
        Returns:
            删除结果
        """
        return parse_response_data(
            requests.post(
                self.use_url("/api/v1/oss/file/delete"),
                data={"fileIDs": file_ids},
                headers=self.header,
            )
        )

    def detail(self, file_id: int):
        """
        获取OSS单个文件详情
        
        Args:
            file_id: 文件ID
            
        Returns:
            文件详情信息，包含文件名、大小、类型、是否在回收站等
        """
        r = requests.post(
            self.use_url("/api/v1/oss/file/detail"),
            data={"fileID": file_id},
            headers=self.header,
        )
        data = parse_response_data(r)
        data["trashed"] = bool(data["trashed"])
        data["type"] = not data["type"]
        return data

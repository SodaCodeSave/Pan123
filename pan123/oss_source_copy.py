import requests

from .utils.request import parse_response_data
from .abstracts import Requestable


class OSSSourceCopy(Requestable):
    """OSS源文件复制管理类，提供OSS文件复制相关的各种操作"""
    
    def copy(self, file_ids: list[int], to_parent_file_id: int):
        """
        创建OSS文件复制任务
        
        Args:
            file_ids: 要复制的文件ID列表
            to_parent_file_id: 目标父文件夹ID
            
        Returns:
            复制任务创建结果
        """
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
        """
        获取OSS复制失败文件列表
        
        Args:
            task_id: 复制任务ID
            limit: 每页数量
            page: 页码
            
        Returns:
            复制失败文件列表
        """
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
        """
        获取OSS复制任务详情
        
        Args:
            task_id: 复制任务ID
            
        Returns:
            复制任务详情，包含进度等信息
        """
        return parse_response_data(
            requests.post(
                self.use_url("/api/v1/oss/source/copy/process"),
                data={"taskID": task_id},
                headers=self.header,
            )
        )

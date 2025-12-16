import requests

from .utils.request import parse_response_data
from .abstracts import Requestable


class OfflineDownload(Requestable):
    """离线下载管理类，提供离线下载相关的各种操作"""
    
    def download(
        self,
        download_url: str,
        file_name: str = "",
        save_path: str = "",
        call_back_url: str = "",
    ):
        """
        创建离线下载任务
        
        Args:
            download_url: 要下载的URL地址
            file_name: 保存的文件名（可选）
            save_path: 保存路径（可选）
            call_back_url: 回调URL（可选）
            
        Returns:
            离线下载任务创建结果，包含taskID等信息
        """
        data = {"url": download_url}
        if file_name:
            data["fileName"] = file_name
        if save_path:
            data["savePath"] = save_path
        if call_back_url:
            data["callBackUrl"] = call_back_url
        return parse_response_data(
            requests.post(
                self.use_url("/api/v1/offline/download"),
                data=data,
                headers=self.header,
            )
        )

    def download_process(self, task_id):
        """
        获取离线下载进度
        
        Args:
            task_id: 离线下载任务ID
            
        Returns:
            离线下载进度信息，包含下载状态、进度百分比等
        """
        return parse_response_data(
            requests.post(
                self.use_url("/api/v1/offline/download/process"),
                data={"taskID": task_id},
                headers=self.header,
            )
        )

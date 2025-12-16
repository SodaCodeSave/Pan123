import requests

from .utils.request import parse_response_data
from .abstracts import Requestable


class User(Requestable):
    """用户管理类，提供用户相关的各种操作"""
    
    def info(self) -> dict:
        """
        获取用户信息
        
        Returns:
            用户信息，包含用户名、存储空间、使用情况等
        """
        return parse_response_data(
            requests.get(
                self.use_url("/api/v1/user/info"),
                headers=self.header,
            )
        )

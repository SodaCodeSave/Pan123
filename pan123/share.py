import json
import requests

from .utils.exceptions import AccessTokenError
from .utils.request import parse_response_data
from .abstracts import Requestable


class Share(Requestable):
    """分享管理类，提供分享链接相关的各种操作"""
    
    def create(
        self,
        share_name: str,
        share_expire: int,
        file_id_list: list,
        share_pwd: str = "",
        traffic_switch: bool = False,
        traffic_limit_switch: bool = False,
        traffic_limit: int = 0,
    ):
        """
        创建分享链接
        
        Args:
            share_name: 分享名称
            share_expire: 分享过期时间（秒）
            file_id_list: 要分享的文件/文件夹ID列表
            share_pwd: 分享密码（可选）
            traffic_switch: 是否开启流量控制
            traffic_limit_switch: 是否开启流量限制
            traffic_limit: 流量限制值
            
        Returns:
            分享结果，包含shareID、shareLink、shareKey等信息
        """
        data: dict = {
            "shareName": share_name,
            "shareExpire": share_expire,
            "fileIDList": file_id_list,
        }
        if share_pwd:
            data["sharePwd"] = share_pwd
        data = Share.apply_traffic_settings(
            data,
            traffic_switch,
            traffic_limit_switch,
            traffic_limit,
        )
        response = requests.post(
            self.use_url("/api/v1/share/create"),
            data=data,
            headers=self.header,
        )
        response_data = json.loads(response.text)
        parse_response_data(response, AccessTokenError)
        return {
            "shareID": response_data["data"]["shareID"],
            "shareLink": f"https://www.123pan.com/s/{response_data['data']['shareKey']}",
            "shareKey": response_data["data"]["shareKey"],
        }

    def list_info(
        self,
        share_id_list: list,
        traffic_switch: bool = False,
        traffic_limit_switch: bool = False,
        traffic_limit: int = 0,
    ):
        """
        获取分享链接列表信息
        
        Args:
            share_id_list: 分享ID列表
            traffic_switch: 是否开启流量控制
            traffic_limit_switch: 是否开启流量限制
            traffic_limit: 流量限制值
            
        Returns:
            分享链接列表信息
        """
        data: dict = Share.apply_traffic_settings(
            {"shareIdList": share_id_list},
            traffic_switch,
            traffic_limit_switch,
            traffic_limit,
        )
        return parse_response_data(
            requests.put(
                self.use_url("/api/v1/share/list/info"),
                data=data,
                headers=self.header,
            )
        )

    def list(self, limit: int, last_share_id: int = 0):
        """
        获取分享链接列表
        
        Args:
            limit: 每页数量
            last_share_id: 最后一个分享ID，用于分页
            
        Returns:
            分享链接列表
        """
        data = {"limit": limit}
        if last_share_id:
            data["lastShareId"] = last_share_id
        return parse_response_data(
            requests.get(
                self.use_url("/api/v1/share/list"), data=data, headers=self.header
            )
        )

    @staticmethod
    def apply_traffic_settings(
        data: dict,
        traffic_switch: bool = False,
        traffic_limit_switch: bool = False,
        traffic_limit: int = 0,
    ) -> dict:
        """
        应用流量设置到分享数据中
        
        Args:
            data: 分享数据字典
            traffic_switch: 是否开启流量控制
            traffic_limit_switch: 是否开启流量限制
            traffic_limit: 流量限制值
            
        Returns:
            应用流量设置后的分享数据字典
            
        Raises:
            ValueError: 当需要限制流量但限制值小于等于0时抛出
        """
        data = data.copy()
        data["trafficSwitch"] = bool(traffic_switch) + 1  # True=1,False=0
        data["trafficLimitSwitch"] = bool(traffic_limit_switch) + 1
        if traffic_limit_switch and traffic_limit <= 0:
            raise ValueError("需要限制流量时，限制值必须大于0")
        return data

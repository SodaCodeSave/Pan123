import requests

from .utils.request import parse_response_data
from .abstracts import Requestable


class DirectLink(Requestable):
    """直链管理类，提供直链相关的各种操作"""
    
    def doPost(self, url: str, data: dict):
        """
        内部辅助方法，用于发送POST请求到直链相关接口
        
        Args:
            url: 接口路径后缀
            data: 请求数据
            
        Returns:
            接口返回结果
        """
        return parse_response_data(
            requests.post(
                self.use_url(f"/api/v1/direct-link/{url}"),
                data=data,
                headers=self.header,
            )
        )
    
    def doForbidIpPost(self, url: str, data: dict):
        """
        内部辅助方法，用于发送POST请求到IP黑名单相关接口
        
        Args:
            url: 接口路径后缀
            data: 请求数据
            
        Returns:
            接口返回结果
        """
        return parse_response_data(
            requests.post(
                self.use_url(f"/api/v1/developer/config/forbide-ip/{url}"),
                data=data,
                headers=self.header,
            )
        )

    def query_transcode(self, ids: list):
        """
        查询直链转码状态
        
        Args:
            ids: 文件ID列表
            
        Returns:
            转码状态查询结果
        """
        return self.doPost("queryTranscode", {"ids": ids})

    def do_transcode(self, ids):
        """
        对直链文件进行转码
        
        Args:
            ids: 文件ID列表
            
        Returns:
            转码操作结果
        """
        return self.doPost("doTranscode", {"ids": ids})

    def get_m3u8(self, file_id):
        """
        获取直链文件的m3u8播放地址
        
        Args:
            file_id: 文件ID
            
        Returns:
            m3u8播放地址信息
        """
        return self.doPost("get/m3u8", {"fileID": file_id})

    def enable(self, file_id):
        """
        启用直链空间
        
        Args:
            file_id: 文件ID
            
        Returns:
            启用直链空间结果
        """
        return self.doPost("enable", {"fileID": file_id})

    def disable(self, file_id):
        """
        禁用直链空间
        
        Args:
            file_id: 文件ID
            
        Returns:
            禁用直链空间结果
        """
        return self.doPost("disable", {"fileID": file_id})

    def list_url(self, file_id):
        """
        获取直链链接
        
        Args:
            file_id: 文件ID
            
        Returns:
            直链链接信息

        """
        url = "url"
        data = {"fileID": file_id}
        return parse_response_data(
            requests.get(
                self.use_url(f"/api/v1/direct-link/{url}"),
                data=data,
                headers=self.header,
            )
        )

    def forbid_ip_switch(self, switch: bool):
        """
        设置IP黑名单开关
        
        Args:
            switch: 开关状态
            
        Returns:
            IP黑名单设置结果
        """
        switch = "1" if switch else "2"
        return self.doPost("forbidIp", {"Status": switch})

    def forbid_ip_update(self, ip_list: list):
        """
        更新IP黑名单列表

        Args:
            ip_list: IP地址列表，最多2000个IPv4地址
            
        Returns:
            操作成功无特定返回数据
        """
        return self.doForbidIpPost("update", {"IpList": ip_list})
    
    def forbid_ip_list(self):
        """
        获取IP黑名单列表
        
        Returns:
            IP黑名单列表和当前设置状态
        """
        return self.doForbidIpPost("list", {}) 
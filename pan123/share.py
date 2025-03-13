import json

import requests

from .utils import AccessTokenError, check_status_code


class Share:
    def __init__(self, base_url, header):
        self.header = header
        self.base_url = base_url

    def create(self, share_name: str, share_expire: int, file_id_list: list, share_pwd=None, traffic_switch=None,
               traffic_limit_switch=None, traffic_limit=None):
        # 构建请求URL
        url = self.base_url + "/api/v1/share/create"
        # 准备请求数据
        data = {
            "shareName": share_name,
            "shareExpire": share_expire,
            "fileIDList": file_id_list
        }
        # 如果分享密码存在，则添加到请求数据中
        if share_pwd:
            data["sharePwd"] = share_pwd
        if traffic_switch:
            if traffic_switch:
                data["trafficSwitch"] = 2
            elif not traffic_switch:
                data["trafficSwitch"] = 1
        if traffic_limit_switch:
            if traffic_limit_switch:
                data["trafficLimitSwitch"] = 2
                if traffic_limit:
                    data["trafficLimit"] = traffic_limit
                else:
                    return ValueError("流量限制开关为True时，流量限制不能为空")
            elif not traffic_limit_switch:
                data["trafficLimitSwitch"] = 1
        # 发送POST请求创建分享
        r = requests.post(url, data=data, headers=self.header)
        # 将响应内容解析为JSON格式
        rdata = json.loads(r.text)
        # 检查HTTP响应状态码
        if r.status_code == 200:
            # 检查接口返回的code
            if rdata["code"] == 0:
                # 返回分享ID、分享链接和分享密钥
                return {
                    "shareID": rdata["data"]["shareID"],
                    "shareLink": f"https://www.123pan.com/s/{rdata['data']['shareKey']}",
                    "shareKey": rdata["data"]["shareKey"]
                }
            else:
                # 如果接口返回的code不为0，抛出AccessTokenError异常
                raise AccessTokenError(rdata)
        else:
            # 如果HTTP响应状态码不是200，抛出HTTPError异常
            raise requests.HTTPError

    def list_info(self, share_id_list: list, traffic_switch: bool = None, traffic_limit_switch: bool = None,
                  traffic_limit: int = None):
        # 构建请求URL
        url = self.base_url + "/api/v1/share/list/info"
        # 准备请求数据
        data = {
            "shareIdList": share_id_list
        }
        # 如果流量开关存在，则添加到请求数据中
        if traffic_switch:
            if traffic_switch:
                data["trafficSwitch"] = 2
            elif not traffic_switch:
                data["trafficSwitch"] = 1
        # 如果流量限制开关存在，则添加到请求数据中
        if traffic_limit_switch:
            if traffic_limit_switch:
                data["trafficLimitSwitch"] = 2
                if traffic_limit:
                    data["trafficLimit"] = traffic_limit
                else:
                    return ValueError("流量限制开关为True时，流量限制不能为空")
            elif not traffic_limit_switch:
                data["trafficLimitSwitch"] = 1

        # 发送POST请求修改分享链接信息
        r = requests.put(url, data=data, headers=self.header)
        # 将响应内容解析为JSON格式
        return check_status_code(r)

    def list(self, limit: int, last_share_id: int = None):
        # 构建请求的URL，将基础URL和分享列表信息的API路径拼接
        url = self.base_url + "/api/v1/share/list"
        # 准备请求数据，设置每页返回的分享数量
        data = {
            "limit": limit
        }
        # 如果传入了lastShareId，将其添加到请求数据中，用于分页查询
        if last_share_id:
            data["lastShareId"] = last_share_id
        # 发送GET请求获取分享列表信息
        r = requests.get(url, data=data, headers=self.header)
        # 将响应内容解析为JSON格式
        return check_status_code(r)

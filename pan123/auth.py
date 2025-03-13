import json

import requests

from .utils import ClientKeyError


def get_access_token(client_id: str, client_secret: str, base_url: str = "https://open-api.123pan.com",
                     header: dict = None):
    # 检查header是否传入，如未传入则使用默认值
    if header is None:
        header = {"Content-Type": "application / json", "Platform": "open_platform"}

    # 构造请求URL
    url = base_url + "/api/v1/access_token"

    # 构造请求数据
    data = {
        "clientID": client_id,
        "clientSecret": client_secret
    }

    # 发送POST请求
    r = requests.post(url, data=data, headers=header)

    # 将响应内容解析为JSON格式
    rdata = json.loads(r.text)

    # 检查HTTP响应状态码
    if r.status_code == 200:
        # 检查API返回的code
        if rdata["code"] == 0:
            # 返回访问令牌
            return rdata['data']['accessToken']
        else:
            # 抛出客户端密钥错误异常
            raise ClientKeyError(rdata)
    else:
        # 抛出HTTP错误异常
        raise requests.HTTPError

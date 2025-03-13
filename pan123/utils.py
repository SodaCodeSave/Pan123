import json

import requests


class ClientKeyError(Exception):
    def __init__(self, r):
        self.r = r
        super().__init__(f"错误的client_id或client_secret，请检查后重试\n{self.r}")


class AccessTokenError(Exception):
    def __init__(self, r):
        self.r = r
        super().__init__(f"错误的access_token，请检查后重试\n{self.r}")


import hashlib


def get_file_md5(file_path):
    """
    计算文件的MD5哈希值。

    :param file_path: 文件的路径
    :return: 文件的MD5哈希值（十六进制字符串）
    """
    md5_hash = hashlib.md5()
    with open(file_path, "rb") as file:
        # 分块读取文件，避免一次性加载大文件到内存中
        for chunk in iter(lambda: file.read(4096), b""):
            md5_hash.update(chunk)
    return md5_hash.hexdigest()


def check_status_code(r):
    # 检查HTTP响应状态码
    if r.status_code == 200:
        # 检查API返回的code
        if json.loads(r.text)["code"] == 0:
            # 返回响应数据中的data部分
            return json.loads(r.text)["data"]
        else:
            # 如果API返回码不为0，抛出AccessTokenError异常
            raise AccessTokenError(json.loads(r.text))
    else:
        # 如果HTTP响应状态码不是200，抛出HTTPError异常
        raise requests.HTTPError(r.text)

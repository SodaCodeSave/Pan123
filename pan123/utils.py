import json
import re

import requests


class ClientKeyError(Exception):
    def __init__(self, r):
        self.r = r
        super().__init__(f"错误的client_id或client_secret，请检查后重试\n{self.r}")


class AccessTokenError(Exception):
    def __init__(self, r):
        self.r = r
        super().__init__(f"错误的access_token，请检查后重试\n{self.r}")

class CloudError(Exception):
    def __init__(self, r):
        self.r = r
        super().__init__(f"{self.r['message']}")

class UrlError(Exception):
    def __init__(self, url_string):
        self.url_string = url_string
        super().__init__(f"错误的URL格式：{self.url_string}")

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
            raise CloudError(json.loads(r.text))
    else:
        # 如果HTTP响应状态码不是200，抛出HTTPError异常
        raise requests.HTTPError(r.text)


def is_valid_url(url_string):
    """
    使用正则表达式验证URL格式，支持HTTP、HTTPS和磁力链接
    
    :param url_string: 要验证的URL字符串
    :return: 如果是有效的URL返回True，否则返回False
    """
    # HTTP/HTTPS URL正则表达式
    # 匹配格式: http://或https://开头，域名，可选的端口号，路径和查询参数
    http_pattern = r'^https?://'  # http://或https://开头
    http_pattern += r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # 域名
    http_pattern += r'localhost|'  # localhost
    http_pattern += r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # IP地址
    http_pattern += r'(?::\d+)?'  # 可选的端口号
    http_pattern += r'(?:/?|[/?]\S+)$'  # 路径和查询参数
    
    # 磁力链接正则表达式
    # 匹配格式: magnet:?xt=urn:btih:哈希值&其他参数
    magnet_pattern = r'^magnet:\?xt=urn:btih:[a-fA-F0-9]{40}'  # 40位哈希值
    magnet_pattern += r'(?:&[a-zA-Z0-9]+=[^&]*)*$'  # 其他参数
    
    # 编译正则表达式（忽略大小写）
    http_regex = re.compile(http_pattern, re.IGNORECASE)
    magnet_regex = re.compile(magnet_pattern, re.IGNORECASE)
    
    # 检查是否为HTTP/HTTPS URL或磁力链接
    return bool(http_regex.match(url_string)) or bool(magnet_regex.match(url_string))
# Python Pan123
# 在使用前，请去123云盘开放平台(https://www.123pan.cn/developer)申请使用权限
# 在邮箱中查询client_id和client_secret，并使用get_access_token函数获取访问令牌

import requests
import json

class ClientKeyError(Exception):
    def __init__(self, r):
        self.r = r
        super().__init__(f"错误的client_id或client_secret，请检查后重试\n{self.r}")

class AccessTokenError(Exception):
    def __init__(self, r):
        self.r = r
        super().__init__(f"错误的access_token，请检查后重试\n{self.r}")

def get_access_token(client_id:str, client_secret:str, base_url:str="https://open-api.123pan.com", header:dict=None):
    """
    获取访问令牌。

    此函数通过POST请求向指定的API端点获取访问令牌。它需要客户端ID和客户端密钥作为参数，
    并可选地接受基础URL和自定义头部信息。

    参数:
    - client_id (str): 客户端ID。
    - client_secret (str): 客户端密钥。
    - base_url (str, 可选): API的基础URL，默认为"https://open-api.123pan.com"。
    - header (dict, 可选): 请求头部信息，默认包含"Content-Type"和"Platform"字段。

    返回:
    - str: 成功时返回访问令牌字符串。

    异常:
    - ClientKeyError: 当API返回的code不为0时抛出。
    - HTTPError: 当HTTP响应状态码不是200时抛出。
    """
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


class Pan123:
    def __init__(self, access_token:str):
        """
        初始化函数，设置API的基础URL和通用请求头。

        :param access_token: str 用户的访问令牌，用于API请求的身份验证。
        """
        # 设置API请求的基础URL
        self.base_url = "https://open-api.123pan.com"

        # 构建请求头，包含内容类型、平台标识和用户授权信息
        self.header = {
            "Content-Type": "application / json",
            "Platform": "open_platform",
            "Authorization": access_token
        }

    def create_share(self, share_name:str, share_expire:int, file_id_list:list, share_pwd=None):
        """
        创建分享链接。

        参数:
        - share_name (str): 分享的名称。
        - share_expire (int): 分享的过期时间。
        - file_id_list (list): 需要分享的文件ID列表。
        - share_pwd (str, 可选): 分享的密码，默认为None。

        返回:
        - dict: 包含分享ID、分享链接和分享密钥的字典。

        异常:
        - AccessTokenError: 如果接口返回的code不为0。
        - HTTPError: 如果HTTP请求的状态码不是200。
        """
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

    def v2_file_list(self, parent_file_id:int, limit:int):
        """
        获取指定父文件夹下的文件列表。

        通过发送GET请求到/api/v2/file/list接口，获取指定父文件夹下的一批文件信息。

        参数:
        - parent_file_id (int): 父文件夹的ID。
        - limit (int): 最多返回的文件数量。

        返回:
        - list: 文件列表，每个文件的信息以字典形式表示。

        异常:
        - AccessTokenError: 如果接口返回的code不为0，则抛出AccessTokenError异常。
        - HTTPError: 如果HTTP请求的响应状态码不是200，则抛出HTTPError异常。
        """
        # 构造请求URL和参数
        url = self.base_url + "/api/v2/file/list"
        data = {
            "parentFileId": parent_file_id,
            "limit": limit
        }

        # 发送GET请求
        r = requests.get(url, data=data, headers=self.header)

        # 将响应内容解析为JSON格式
        rdata = json.loads(r.text)

        # 检查HTTP响应状态码
        if r.status_code == 200:
            # 检查接口返回的code
            if rdata["code"] == 0:
                # 返回文件列表
                return rdata["data"]["fileList"]
            else:
                # 如果code不为0，抛出AccessTokenError异常
                raise AccessTokenError(rdata)
        else:
            # 如果HTTP响应状态码不是200，抛出HTTPError异常
            raise requests.HTTPError

    def v1_file_mkdir(self, name:str, parent_id:int):
        """
        创建文件夹

        通过发送GET请求到服务器，创建一个新文件夹

        参数:
        name (str): 要创建的文件夹的名称
        parent_id (int): 新文件夹的父目录ID

        返回:
        新创建文件夹的相关信息，具体结构取决于服务器返回的数据

        异常:
        AccessTokenError: 当服务器返回的code不为0时抛出
        HTTPError: 当HTTP响应状态码不是200时抛出
        """
        # 构造请求URL和参数
        url = self.base_url + "/upload/v1/file/mkdir"
        data = {
            "name": name,
            "parentID": parent_id
        }

        # 发送GET请求
        r = requests.get(url, data=data, headers=self.header)

        # 将响应内容解析为JSON格式
        rdata = json.loads(r.text)

        # 检查HTTP响应状态码
        if r.status_code == 200:
            # 检查服务器返回的code
            if rdata["code"] == 0:
                # 如果code为0，表示操作成功，返回数据
                return rdata["data"]
            else:
                # 如果code不为0，抛出AccessTokenError异常
                raise AccessTokenError(rdata)
        else:
            # 如果HTTP响应状态码不是200，抛出HTTPError异常
            raise requests.HTTPError
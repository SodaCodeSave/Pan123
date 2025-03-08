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

class Pan123:
    def __init__(self, access_token:str):
        # 设置API请求的基础URL
        self.base_url = "https://open-api.123pan.com"

        # 构建请求头，包含内容类型、平台标识和用户授权信息
        self.header = {
            "Content-Type": "application / json",
            "Platform": "open_platform",
            "Authorization": access_token
        }

    def create_share(self, share_name:str, share_expire:int, file_id_list:list, share_pwd=None):
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
    
    def share_list_info(self, shareIdList:list, trafficSwitch:bool=None, trafficLimitSwitch:bool=None, trafficLimit:int=None):
        # 构建请求URL
        url = self.base_url + "/api/v1/share/list/info"
        # 准备请求数据
        data = {
            "shareIdList": shareIdList
        }
        # 如果流量开关存在，则添加到请求数据中
        if trafficSwitch:
            if trafficSwitch == True:
                data["trafficSwitch"] = 2
            elif trafficSwitch == False:
                data["trafficSwitch"] = 1
        # 如果流量限制开关存在，则添加到请求数据中
        if trafficLimitSwitch:
            if trafficLimitSwitch == True:
                data["trafficLimitSwitch"] = 2
                if trafficLimit:
                    data["trafficLimit"] = trafficLimit
                else:
                    return ValueError("流量限制开关为True时，流量限制不能为空")
            elif trafficLimitSwitch == False:
                data["trafficLimitSwitch"] = 1

        # 发送POST请求修改分享链接信息
        r = requests.put(url, data=data, headers=self.header)
        # 将响应内容解析为JSON格式
        return check_status_code(r)
        
    def share_list(self, limit:int, lastShareId:int=None):
        # 构建请求的URL，将基础URL和分享列表信息的API路径拼接
        url = self.base_url + "/api/v1/share/list"
        # 准备请求数据，设置每页返回的分享数量
        data = {
            "limit": limit   
        }
        # 如果传入了lastShareId，将其添加到请求数据中，用于分页查询
        if lastShareId:
            data["lastShareId"] = lastShareId
        # 发送GET请求获取分享列表信息
        r = requests.get(url, data=data, headers=self.header)
        # 将响应内容解析为JSON格式
        return check_status_code(r)
        
    def file_list(self, parent_file_id:int, limit:int):
        # 构造请求URL和参数
        url = self.base_url + "/api/v2/file/list"
        data = {
            "parentFileId": parent_file_id,
            "limit": limit
        }

        # 发送GET请求
        r = requests.get(url, data=data, headers=self.header)

        # 将响应内容解析为JSON格式
        return check_status_code(r)

    def file_mkdir(self, name:str, parent_id:int):
        # 构造请求URL和参数
        url = self.base_url + "/upload/v1/file/mkdir"
        data = {
            "name": name,
            "parentID": parent_id
        }

        # 发送GET请求
        r = requests.get(url, data=data, headers=self.header)

        # 将响应内容解析为JSON格式
        return check_status_code(r)
    
    def file_create(self, parentFileID:int, filename:str, etag:str, size:int, duplicate:int=None):
        # 构造请求URL
        url = self.base_url + "/upload/v1/file/create"
        # 准备请求数据
        data = {
            "parentFileID": parentFileID,
            # 文件名
            "filename": filename,
            # 文件的etag
            "etag": etag,
            # 文件大小
            "size": size
        }
        # 如果传入了重复处理方式参数，则添加到请求数据中
        if duplicate:
            data["duplicate"] = duplicate
        # 发送POST请求
        r = requests.post(url, data=data, headers=self.header)
        # 将响应内容解析为JSON格式
        return check_status_code(r)
        
    def file_get_upload_url(self, preuploadID:str, sliceNo:int):
        # 构造请求URL
        url = self.base_url + "/upload/v1/file/get_upload_url"
        # 准备请求数据
        data = {
            "preuploadID": preuploadID,
            "sliceNo": sliceNo
        }
        # 发送POST请求
        r = requests.post(url, data=data, headers=self.header)
        # 将响应内容解析为JSON格式
        return check_status_code(r)
    
    def file_upload(self, url:str, data:bytes):
        # 发送Put请求
        r = requests.put(url, files=data, headers=self.header)
        # 将响应内容解析为JSON格式
        return check_status_code(r)
    
    def file_list_upload_parts(self, preuploadID:str):
        # 构造请求URL
        url = self.base_url + "/upload/v1/file/list_upload_parts"
        # 准备请求数据
        data = {
            "preuploadID": preuploadID
        }
        # 发送POST请求
        r = requests.post(url, data=data, headers=self.header)
        # 将响应内容解析为JSON格式
        return check_status_code(r)
    
    def file_upload_complete(self, preuploadID:str):
        # 构造请求URL
        url = self.base_url + "/upload/v1/file/upload_complete"
        # 准备请求数据
        data = {
            "preuploadID": preuploadID
        }
        # 发送POST请求
        r = requests.post(url, data=data, headers=self.header)
        # 将响应内容解析为JSON格式
        return check_status_code(r)
    
    def file_upload_async_result(self, preuploadID:str):
        # 构造请求URL
        url = self.base_url + "/upload/v1/file/upload_async_result"
        # 准备请求数据
        data = {
            "preuploadID": preuploadID
        }
        # 发送POST请求
        r = requests.post(url, data=data, headers=self.header)
        # 将响应内容解析为JSON格式
        return check_status_code(r)
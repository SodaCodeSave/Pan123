# Python Pan123
# 在使用前，请去123云盘开放平台(https://www.123pan.cn/developer)申请使用权限
# 在邮箱中查询client_id和client_secret，并使用get_access_token函数获取访问令牌

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


class Pan123:
    def __init__(self, access_token: str):
        # 设置API请求的基础URL
        self.base_url = "https://open-api.123pan.com"

        # 构建请求头，包含内容类型、平台标识和用户授权信息
        self.header = {
            "Content-Type": "application / json",
            "Platform": "open_platform",
            "Authorization": access_token
        }

    def create_share(self, share_name: str, share_expire: int, file_id_list: list, share_pwd=None):
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

    def share_list_info(self, share_id_list: list, traffic_switch: bool = None, traffic_limit_switch: bool = None,
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

    def share_list(self, limit: int, last_share_id: int = None):
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

    def file_list(self, parent_file_id: int, limit: int):
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

    def file_mkdir(self, name: str, parent_id: int):
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

    def file_create(self, preupload_id: int, filename: str, etag: str, size: int, duplicate: int = None):
        # 构造请求URL
        url = self.base_url + "/upload/v1/file/create"
        # 准备请求数据
        data = {
            "parentFileID": preupload_id,
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

    def file_get_upload_url(self, preupload_id: str, slice_no: int):
        # 构造请求URL
        url = self.base_url + "/upload/v1/file/get_upload_url"
        # 准备请求数据
        data = {
            "preuploadID": preupload_id,
            "sliceNo": slice_no
        }
        # 发送POST请求
        r = requests.post(url, data=data, headers=self.header)
        # 将响应内容解析为JSON格式
        return check_status_code(r)["presignedURL"]

    def file_list_upload_parts(self, preupload_id: str):
        # 构造请求URL
        url = self.base_url + "/upload/v1/file/list_upload_parts"
        # 准备请求数据
        data = {
            "preuploadID": preupload_id
        }
        # 发送POST请求
        r = requests.post(url, data=data, headers=self.header)
        # 将响应内容解析为JSON格式
        return check_status_code(r)

    def file_upload_complete(self, preupload_id: str):
        # 构造请求URL
        url = self.base_url + "/upload/v1/file/upload_complete"
        # 准备请求数据
        data = {
            "preuploadID": preupload_id
        }
        # 发送POST请求
        r = requests.post(url, data=data, headers=self.header)
        # 将响应内容解析为JSON格式
        return check_status_code(r)

    def file_upload_async_result(self, preupload_id: str):
        # 构造请求URL
        url = self.base_url + "/upload/v1/file/upload_async_result"
        # 准备请求数据
        data = {
            "preuploadID": preupload_id
        }
        # 发送POST请求
        r = requests.post(url, data=data, headers=self.header)
        # 将响应内容解析为JSON格式
        return check_status_code(r)

    def file_upload(self, preupload_id, file_path):
        # 一键上传文件
        import os
        import math
        upload_data_parts = {}
        f = self.file_create(preupload_id, os.path.basename(file_path), get_file_md5(file_path),
                             os.stat(file_path).st_size)
        num_slices = math.ceil(os.stat(file_path).st_size / f["sliceSize"])
        with open(file_path, "rb") as fi:
            for i in range(1, num_slices + 1):
                url = self.file_get_upload_url(f["preuploadID"], i)
                chunk = fi.read(f["sliceSize"])
                md5 = hashlib.md5(chunk).hexdigest()
                # 发送Put请求
                requests.put(url, data=chunk)
                upload_data_parts[i] = {
                    "md5": md5,
                    "size": len(chunk),
                }
        if not os.stat(file_path).st_size <= f["sliceSize"]:
            parts = self.file_list_upload_parts(f["preuploadID"])
            for i in parts["parts"]:
                part = i["partNumber"]
                if upload_data_parts[i]["md5"] == part["etag"] and upload_data_parts[i]["size"] == part["size"]:
                    pass
                else:
                    raise requests.HTTPError
        self.file_upload_complete(f["preuploadID"])

    def file_rename(self, rename_dict: dict):
        # 构造请求URL
        url = self.base_url + "/api/v1/file/rename"
        # 准备请求数据
        rename_list = []
        for i in rename_dict.keys():
            rename_list.append(f"{i}|{rename_dict[i]}")
        data = {
            "renameList": rename_list
        }
        # 发送POST请求
        r = requests.post(url, data=data, headers=self.header)
        return check_status_code(r)

    def file_move(self, file_id_list: list, to_parent_file_id: int):
        # 构造请求URL
        url = self.base_url + "/api/v1/file/move"
        # 准备请求数据
        data = {
            "fileIDs": file_id_list,
            "toParentFileID": to_parent_file_id
        }
        # 发送POST请求
        r = requests.post(url, data=data, headers=self.header)
        return check_status_code(r)

    def file_trash(self, file_ids):
        url = self.base_url + "/api/v1/file/trash"
        data = {
            "fileIDs": file_ids
        }
        r = requests.post(url, data=data, headers=self.header)
        return check_status_code(r)

    def file_recover(self, file_ids):
        url = self.base_url + "/api/v1/file/recover"
        data = {
            "fileIDs": file_ids
        }
        r = requests.post(url, data=data, headers=self.header)
        return check_status_code(r)

    def file_delete(self, file_ids):
        url = self.base_url + "/api/v1/file/delete"
        data = {
            "fileIDs": file_ids
        }
        r = requests.post(url, data=data, headers=self.header)
        return check_status_code(r)

    def file_detail(self, file_id):
        url = self.base_url + "/api/v1/file/detail"
        data = {
            "fileID": file_id
        }
        r = requests.post(url, data=data, headers=self.header)
        data = check_status_code(r)
        if data["trashed"] == 1:
            data["trashed"] = True
        else:
            data["trashed"] = False
        if data["type"] == 1:
            data["type"] = "folder"
        else:
            data["type"] = "file"
        return data

    def user_info(self):
        url = self.base_url + "/api/v1/user/info"
        r = requests.post(url, headers=self.header)
        return check_status_code(r)

    def offline_download(self, download_url, file_name=None, save_path=None, call_back_url=None):
        url = self.base_url + "/api/v1/offline/download"
        data = {
            "url": download_url
        }
        if file_name:
            data["fileName"] = file_name
        if save_path:
            data["savePath"] = save_path
        if call_back_url:
            data["callBackUrl"] = call_back_url
        r = requests.post(url, data=data, headers=self.header)
        return check_status_code(r)

    def offline_download_process(self, task_id):
        url = self.base_url + "/api/v1/offline/download/process"
        data = {
            "taskID": task_id
        }
        r = requests.post(url, data=data, headers=self.header)
        return check_status_code(r)

    # 直链部分 By-@狸雪花
    def query_transcode(self, ids):  # 查询转码进度
        url = self.base_url + "/api/v1/direct-link/queryTranscode"
        data = {
            "ids": ids
        }
        r = requests.post(url, data=data, headers=self.header)
        return check_status_code(r)

    def do_transcode(self, ids):  # 发起直链转码
        url = self.base_url + "/api/v1/direct-link/doTranscode"
        data = {
            "ids": ids,
        }
        r = requests.post(url, data=data, headers=self.header)
        return check_status_code(r)

    def get_direct_link_m3u8(self, file_id):  # 获取直链直连
        url = self.base_url + "/api/v1/direct-link/get/m3u8"
        data = {
            "fileID": file_id,
        }
        r = requests.post(url, data=data, headers=self.header)
        return check_status_code(r)

    def direct_link_enable(self, file_id):  # 开启直链功能
        url = self.base_url + "/api/v1/direct-link/enable"
        data = {
            "fileID": file_id,
        }
        r = requests.post(url, data=data, headers=self.header)
        return check_status_code(r)

    def direct_link_disable(self, file_id):  # 关闭直链功能
        url = self.base_url + "/api/v1/direct-link/disable"
        data = {
            "fileID": file_id,
        }
        r = requests.post(url, data=data, headers=self.header)
        return check_status_code(r)

    def direct_list_url(self, file_id):  # 获取直链地址
        url = self.base_url + "/api/v1/direct-link/url"
        data = {
            "fileID": file_id,
        }
        r = requests.post(url, data=data, headers=self.header)
        return check_status_code(r)
    # 喵呜，直连部分写完了喵
    #视频转码部分 By-@狸雪花
    def transcode_folder_info(self):#获取转码文件夹信息
        url = self.base_url + "/api/v1/transcode/folder/info"
        r = requests.post(url, headers=self.header)
        return check_status_code(r)
    def transcode_file_list(self, parentfileid, limit, bussinesstype, searchdata=None, searchmode=None, lastfileld=None):#获取转码文件列表
        url = self.base_url + "/api/v2/file/list"
        data = {
            "parentFileId": parentfileid,
            "limit": limit,
            "businessType": bussinesstype,
        }
        if searchdata:
            data["searchData"] = searchdata
        if searchmode:
            data["searchMode"] = searchmode
        if lastfileld:
            data["lastFileld"] = lastfileld
        r = requests.post(url, data=data, headers=self.header)
        return check_status_code(r)
    def get_transcode_video(self, parentfileid, limit, searchdata=None, searchmode=None, lastfileid=None, category=2):#获取转码视频文件
        url = self.base_url + "/api/v2/file/list"
        data = {
            "parentFileId": parentfileid,
            "limit": limit,
            "category": category,
        }
        if searchdata:
            data["searchData"] = searchdata
        if searchmode:
            data["searchMode"] = searchmode
        if lastfileid:
            data["lastFileId"] = lastfileid
        r = requests.get(url, data=data, headers=self.header)
        return check_status_code(r)
    def transcode_from_cloud_disk(self, fileid):#从网盘转码
        url = self.base_url + "/api/v1/transcode/upload/from_cloud_disk"
        data = {
            "fileId": fileid,
        }
        r = requests.post(url, data=data, headers=self.header)
        return check_status_code(r)
    def transcode_delete(self, fileid, businesstype, trashed):#删除转码文件
        url = self.base_url + "/api/v1/transcode/delete"
        data = {
            "fileId": fileid,
            "businessType": businesstype,
            "trashed": trashed,
        }
        r = requests.post(url, data=data, headers=self.header)
        return check_status_code(r)
    def transcode_video_resolution(self, fileid):#获取转码视频分辨率
        url = self.base_url + "/api/v1/transcode/video/resolution"
        data = {
            "fileId": fileid,
        }
        r = requests.post(url, data=data, headers=self.header)
        return check_status_code(r)
    def transcode_video(self, fileid, codecname, videotime, resoulutions):#转码视频
        url = self.base_url + "/api/v1/transcode/video"
        data = {
            "fileId": fileid,
            "codecName": codecname,
            "videoTime": videotime,
            "resoulutions": resoulutions,
        }
        r = requests.post(url, data=data, headers=self.header)
        return check_status_code(r)
    #嗷呜，我是一只小猫咪，喵喵喵！
    def transcode_video_record(self, fileid):#转码视频记录
        url = self.base_url + "/api/v1/transcode/video/record"
        data = {
            "fileId": fileid,
        }
        r = requests.post(url, data=data, headers=self.header)
        return check_status_code(r)
    def transcode_video_result(self, fileid):#转码视频结果
        url = self.base_url + "/api/v1/transcode/video/result"
        data = {
            "fileId": fileid,
        }
        r = requests.post(url, data=data, headers=self.header)
        return check_status_code(r)
    def transcode_file_download(self, fileid):#转码文件下载
        url = self.base_url + "/api/v1/transcode/file/download"
        data = {
            "fileId": fileid,
        }
        r = requests.post(url, data=data, headers=self.header)
        return check_status_code(r)
    def transcode_m3u8_ts_download(self, fileid, resolution, type, tsname=None):#转码m3u8/ts下载
        url = self.base_url + "/api/v1/transcode/m3u8_ts/download"
        data = {
            "fileId": fileid,
            "resolution": resolution,
            "type": type,
        }
        if tsname:
            data["tsName"] = tsname
        r = requests.post(url, data=data, headers=self.header)
        return check_status_code(r)
    def transcode_file_download_all(self, fileid, zipname):#转码文件下载全部
        url = self.base_url + "/api/v1/transcode/file/download_all"
        data = {
            "fileId": fileid,
            "zipName": zipname,
        }
        r = requests.post(url, data=data, headers=self.header)
        return check_status_code(r)
#嗷呜，视频转码完成，喵喵喵！

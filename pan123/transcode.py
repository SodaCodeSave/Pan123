import requests

from .utils import check_status_code


class Transcode:
    def __init__(self, base_url, header):
        self.header = header
        self.base_url = base_url

    # 视频转码部分 By-@狸雪花
    def folder_info(self):  # 获取转码文件夹信息
        url = self.base_url + "/api/v1/transcode/folder/info"
        r = requests.post(url, headers=self.header)
        return check_status_code(r)

    def file_list(self, parent_file_id, limit, business_type, search_data=None, search_mode=None,
                  last_file_id=None):  # 获取转码文件列表
        url = self.base_url + "/api/v2/file/list"
        data = {
            "parentFileId": parent_file_id,
            "limit": limit,
            "businessType": business_type,
        }
        if search_data:
            data["searchData"] = search_data
        if search_mode:
            data["searchMode"] = search_mode
        if last_file_id:
            data["lastFileId"] = last_file_id
        r = requests.post(url, data=data, headers=self.header)
        return check_status_code(r)

    def get_video(self, parent_file_id, limit, searchdata=None, search_mode=None, last_file_id=None,
                  category=2):  # 获取转码视频文件
        url = self.base_url + "/api/v2/file/list"
        data = {
            "parentFileId": parent_file_id,
            "limit": limit,
            "category": category,
        }
        if searchdata:
            data["searchData"] = searchdata
        if search_mode:
            data["searchMode"] = search_mode
        if last_file_id:
            data["lastFileId"] = last_file_id
        r = requests.get(url, data=data, headers=self.header)
        return check_status_code(r)

    def from_cloud_disk(self, file_id):  # 从网盘转码
        url = self.base_url + "/api/v1/transcode/upload/from_cloud_disk"
        data = {
            "fileId": file_id,
        }
        r = requests.post(url, data=data, headers=self.header)
        return check_status_code(r)

    def delete(self, file_id, business_type, trashed):  # 删除转码文件
        url = self.base_url + "/api/v1/transcode/delete"
        data = {
            "fileId": file_id,
            "businessType": business_type,
            "trashed": trashed,
        }
        r = requests.post(url, data=data, headers=self.header)
        return check_status_code(r)

    def video_resolution(self, file_id):  # 获取转码视频分辨率
        url = self.base_url + "/api/v1/transcode/video/resolution"
        data = {
            "fileId": file_id,
        }
        r = requests.post(url, data=data, headers=self.header)
        return check_status_code(r)

    def video(self, file_id, codec_name, video_time, resolutions):  # 转码视频
        url = self.base_url + "/api/v1/transcode/video"
        data = {
            "fileId": file_id,
            "codecName": codec_name,
            "videoTime": video_time,
            "resolutions": resolutions,
        }
        r = requests.post(url, data=data, headers=self.header)
        return check_status_code(r)

    # 嗷呜，我是一只小猫咪，喵喵喵！
    def video_record(self, file_id):  # 转码视频记录
        url = self.base_url + "/api/v1/transcode/video/record"
        data = {
            "fileId": file_id,
        }
        r = requests.post(url, data=data, headers=self.header)
        return check_status_code(r)

    def video_result(self, file_id):  # 转码视频结果
        url = self.base_url + "/api/v1/transcode/video/result"
        data = {
            "fileId": file_id,
        }
        r = requests.post(url, data=data, headers=self.header)
        return check_status_code(r)

    def file_download(self, file_id):  # 转码文件下载
        url = self.base_url + "/api/v1/transcode/file/download"
        data = {
            "fileId": file_id,
        }
        r = requests.post(url, data=data, headers=self.header)
        return check_status_code(r)

    def m3u8_ts_download(self, fileid, resolution, file_type, ts_name=None):  # 转码m3u8/ts下载
        url = self.base_url + "/api/v1/transcode/m3u8_ts/download"
        data = {
            "fileId": fileid,
            "resolution": resolution,
            "type": file_type,
        }
        if ts_name:
            data["tsName"] = ts_name
        r = requests.post(url, data=data, headers=self.header)
        return check_status_code(r)

    def file_download_all(self, fileid, zip_name):  # 转码文件下载全部
        url = self.base_url + "/api/v1/transcode/file/download_all"
        data = {
            "fileId": fileid,
            "zipName": zip_name,
        }
        r = requests.post(url, data=data, headers=self.header)
        return check_status_code(r)
    # 嗷呜，视频转码完成，喵喵喵！

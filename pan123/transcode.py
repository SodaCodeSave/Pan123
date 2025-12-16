import requests

from .utils.request import parse_response_data
from .abstracts import Requestable
from .costants import SearchMode, VideoFileType


class Transcode(Requestable):
    """视频转码管理类，提供视频转码相关的各种操作"""
    
    def folder_info(self, file_id: int) -> dict:
        """
        获取转码文件夹信息
        
        Args:
            file_id: 文件夹ID
            
        Returns:
            文件夹信息
        """
        return parse_response_data(
            requests.post(
                self.use_url("/api/v1/transcode/folder/info"),
                headers=self.header,
                data={"fileID": file_id},
            )
        )

    def file_list(
        self,
        parent_file_id: int,
        limit: int,
        search_data: str = "",
        search_mode: SearchMode = SearchMode.NORMAL,
        last_file_id: int = 0,
    ) -> list[dict]:
        """
        获取转码文件列表
        
        Args:
            parent_file_id: 父文件夹ID
            limit: 每页数量
            search_data: 搜索关键字
            search_mode: 搜索模式
            last_file_id: 最后一个文件ID，用于分页
            
        Returns:
            转码文件列表
        """
        data: dict = {
            "parentFileId": parent_file_id,
            "limit": limit,
            "businessType": 2,
        }
        if search_data:
            data["searchData"] = search_data
        if search_mode:
            data["searchMode"] = search_mode
        if last_file_id:
            data["lastFileId"] = last_file_id
        return parse_response_data(
            requests.post(
                self.use_url("/api/v2/file/list"),
                data=data,
                headers=self.header,
            )
        )

    def from_cloud_disk(self, file_id: int):
        """
        从云盘空间上传视频到转码空间
        
        Args:
            file_id: 云盘文件ID
            
        Returns:
            上传结果
        """
        return parse_response_data(
            requests.post(
                self.use_url("/api/v1/transcode/upload/from_cloud_disk"),
                data={"fileId": file_id},
                headers=self.header,
            )
        )

    def delete(self, file_id: int, original: bool = False, transcoded: bool = False):
        """
        删除转码视频
        
        Args:
            file_id: 视频文件ID
            original: 是否删除原文件
            transcoded: 是否删除转码文件
            
        Returns:
            删除结果
        """
        return parse_response_data(
            requests.post(
                self.use_url("/api/v1/transcode/delete"),
                data={
                    "fileId": file_id,
                    "businessType": 2,
                    "trashed": original + transcoded,
                },
                headers=self.header,
            )
        )

    def video_resolution(self, file_id: int):
        """
        获取视频文件可转码的分辨率
        
        Args:
            file_id: 视频文件ID
            
        Returns:
            可转码的分辨率列表
        """
        return parse_response_data(
            requests.post(
                self.use_url("/api/v1/transcode/video/resolution"),
                data={"fileId": file_id},
                headers=self.header,
            )
        )

    def video(
        self,
        file_id: int,
        codec_name: str,
        video_time: str,
        resolutions: list[int],
    ):
        """
        提交视频转码任务
        
        Args:
            file_id: 视频文件ID
            codec_name: 编码名称
            video_time: 视频时长
            resolutions: 转码分辨率列表
            
        Returns:
            转码任务提交结果
        """
        return parse_response_data(
            requests.post(
                self.use_url("/api/v1/transcode/video"),
                data={
                    "fileId": file_id,
                    "codecName": codec_name,
                    "videoTime": video_time,
                    "resolutions": ",".join(map(lambda x: f"{x}P", resolutions)),
                },
                headers=self.header,
            )
        )

    def video_record(self, file_id: int):
        """
        查询某个视频的转码记录
        
        Args:
            file_id: 视频文件ID
            
        Returns:
            转码记录
        """
        return parse_response_data(
            requests.post(
                self.use_url("/api/v1/transcode/video/record"),
                data={"fileId": file_id},
                headers=self.header,
            )
        )

    def video_result(self, file_id: int):
        """
        查询某个视频的转码结果
        
        Args:
            file_id: 视频文件ID
            
        Returns:
            转码结果
        """
        return parse_response_data(
            requests.post(
                self.use_url("/api/v1/transcode/video/result"),
                data={"fileId": file_id},
                headers=self.header,
            )
        )

    def file_download(self, file_id: int):
        """
        原文件下载
        
        Args:
            file_id: 视频文件ID
            
        Returns:
            原文件下载链接
        """
        return parse_response_data(
            requests.post(
                self.use_url("/api/v1/transcode/file/download"),
                data={"fileId": file_id},
                headers=self.header,
            )
        )

    def m3u8_ts_download(
        self,
        file_id: int,
        resolution: int,
        file_type: VideoFileType,
        ts_name: str = "",
    ):
        """
        单个转码文件下载（m3u8或ts）
        
        Args:
            file_id: 视频文件ID
            resolution: 转码分辨率
            file_type: 文件类型（m3u8或ts）
            ts_name: ts文件名（可选，仅当file_type为ts时使用）
            
        Returns:
            转码文件下载链接
        """
        data = {
            "fileId": file_id,
            "resolution": f"{resolution}P",
            "type": file_type,
        }
        if ts_name:
            data["tsName"] = ts_name
        return parse_response_data(
            requests.post(
                self.use_url("/api/v1/transcode/m3u8_ts/download"),
                data=data,
                headers=self.header,
            )
        )

    def file_download_all(self, file_id: int, zip_name: str):
        """
        某个视频全部转码文件下载
        
        Args:
            file_id: 视频文件ID
            zip_name: 压缩包名称
            
        Returns:
            全部转码文件的压缩包下载链接
        """
        return parse_response_data(
            requests.post(
                self.use_url("/api/v1/transcode/file/download_all"),
                data={
                    "fileId": file_id,
                    "zipName": zip_name,
                },
                headers=self.header,
            )
        )

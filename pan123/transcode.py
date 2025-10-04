import requests

from .utils.request import parse_response_data
from .abstracts import Requestable
from .costants import SearchMode, VideoFileType


class Transcode(Requestable):
    def folder_info(self, file_id: int) -> dict:
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
        return parse_response_data(
            requests.post(
                self.use_url("/api/v1/transcode/upload/from_cloud_disk"),
                data={"fileId": file_id},
                headers=self.header,
            )
        )

    def delete(self, file_id: int, original: bool = False, transcoded: bool = False):
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
        return parse_response_data(
            requests.post(
                self.use_url("/api/v1/transcode/video/record"),
                data={"fileId": file_id},
                headers=self.header,
            )
        )

    def video_result(self, file_id: int):
        return parse_response_data(
            requests.post(
                self.use_url("/api/v1/transcode/video/result"),
                data={"fileId": file_id},
                headers=self.header,
            )
        )

    def file_download(self, file_id: int):
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

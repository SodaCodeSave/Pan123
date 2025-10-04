# Python Pan123
# 在使用前，请去123云盘开放平台(https://www.123pan.cn/developer)申请使用权限
# 在邮箱中查询client_id和client_secret，并使用get_access_token函数获取访问令牌

from .abstracts import Requestable

from .share import Share
from .file import File
from .user import User
from .offline_download import OfflineDownload
from .direct_link import DirectLink
from .transcode import Transcode
from .oss import OSS


class Pan123(Requestable):
    def __init__(self, access_token: str):
        super().__init__(
            "https://open-api.123pan.com",
            {
                "Content-Type": "application/json",
                "Platform": "open_platform",
                "Authorization": "Bearer " + access_token,
            },
        )
        self.share = Share(self.base_url, self.header)
        self.file = File(self.base_url, self.header)
        self.user = User(self.base_url, self.header)
        self.offline_download = OfflineDownload(self.base_url, self.header)
        self.direct_link = DirectLink(self.base_url, self.header)
        self.transcode = Transcode(self.base_url, self.header)
        self.oss = OSS(self.base_url, self.header)

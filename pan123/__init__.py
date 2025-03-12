# Python Pan123
# 在使用前，请去123云盘开放平台(https://www.123pan.cn/developer)申请使用权限
# 在邮箱中查询client_id和client_secret，并使用get_access_token函数获取访问令牌

from .utils import AccessTokenError, get_file_md5, check_status_code


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

        from .share import Share
        self.share = Share(self.base_url, self.header)
        from .file import File
        self.file = File(self.base_url, self.header)
        from .user import User
        self.user = User(self.base_url, self.header)
        from .offline_download import OfflineDownload
        self.offline_download = OfflineDownload(self.base_url, self.header)
        from .direct_link import DirectLink
        self.direct_link = DirectLink(self.base_url, self.header)
        from .transcode import Transcode
        self.transcode = Transcode(self.base_url, self.header)
        from .oss import OSS
        self.oss = OSS(self.base_url, self.header)
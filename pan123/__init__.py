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
from .utils.dict_util import merge_dict


class Pan123(Requestable):
    """123云盘开放平台Python SDK的主类，提供对123云盘各种功能的访问接口
    
    使用前请先去123云盘开放平台(https://www.123pan.cn/developer)申请使用权限，
    在邮箱中查询client_id和client_secret，并使用get_access_token函数获取访问令牌。
    """
    
    def __init__(
        self,
        access_token: str,
        base_url: str = "https://open-api.123pan.com",
        header: dict = {
            "Content-Type": "application/json",
            "Platform": "open_platform",
        },
    ):
        """
        初始化Pan123客户端
        
        Args:
            access_token: 访问令牌，通过OAuth2.0授权获取
            base_url: API基础URL，默认为123云盘开放平台官方地址
            header: 自定义请求头，将与默认请求头合并
            
        Attributes:
            share: 分享管理对象，提供分享链接相关操作
            file: 文件管理对象，提供文件相关操作
            user: 用户管理对象，提供用户信息相关操作
            offline_download: 离线下载对象，提供离线下载相关操作
            direct_link: 直链管理对象，提供直链相关操作
            transcode: 视频转码对象，提供视频转码相关操作
            oss: OSS存储对象，提供OSS相关操作
        """
        super().__init__(
            base_url,
            merge_dict(header, {"Authorization": f"Bearer {access_token}"}),
        )
        self.share = Share(self.base_url, self.header)
        self.file = File(self.base_url, self.header)
        self.user = User(self.base_url, self.header)
        self.offline_download = OfflineDownload(self.base_url, self.header)
        self.direct_link = DirectLink(self.base_url, self.header)
        self.transcode = Transcode(self.base_url, self.header)
        self.oss = OSS(self.base_url, self.header)

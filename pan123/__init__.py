from .abstracts import Requestable
from .share import Share
from .file import File
from .user import User
from .offline_download import OfflineDownload
from .direct_link import DirectLink
from .transcode import Transcode
from .oss import OSS
from .auth import Auth
from .utils.dict_util import merge_dict

import json
import time
from pathlib import Path
from datetime import datetime, timezone, timedelta  # 仅使用标准库

class Pan123(Requestable):
    """
    123云盘开放平台Python SDK的主类，提供对123云盘各种功能的访问接口
    
    使用前请先去123云盘开放平台(https://www.123pan.cn/developer)申请使用权限，
    在邮箱中查询client_id和client_secret，并使用get_access_token函数获取访问令牌。
    """

    def __init__(
        self,
        client_id: str = None,
        client_secret: str = None,
        token_path: str | Path = ".token_info.json",
        base_url: str = "https://open-api.123pan.com",
        header: dict = None,
    ):
        """
        初始化Pan123客户端
        
        Args:
            client_id: 客户端ID，从123云盘开放平台获取
            client_secret: 客户端密钥，从123云盘开放平台获取
            token_path: 本地存储Token信息的文件路径，默认为".token_info.json"
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
        self.client_id = client_id
        self.client_secret = client_secret
        self.token_path = Path(token_path) if not isinstance(token_path, Path) else token_path

        # 1. 初始化基础 Header
        default_header = {
            "Content-Type": "application/json",
            "Platform": "open_platform",
        }
        final_header = merge_dict(default_header, header) if header else default_header
        
        super().__init__(base_url, final_header)

        # 2. 初始化 Auth
        self.auth = Auth(self.base_url, self.header)
        
        # 3. 尝试认证
        self._authenticate_session()

        # 4. 初始化业务模块
        self.share = Share(self.base_url, self.header)
        self.file = File(self.base_url, self.header)
        self.user = User(self.base_url, self.header)
        self.offline_download = OfflineDownload(self.base_url, self.header)
        self.direct_link = DirectLink(self.base_url, self.header)
        self.transcode = Transcode(self.base_url, self.header)
        self.oss = OSS(self.base_url, self.header)

    def _authenticate_session(self):
        token = self._load_valid_token_from_file()
        
        if token:
            self.header["Authorization"] = f"Bearer {token}"
        elif self.client_id and self.client_secret:
            print("Token 不存在或已过期，正在执行自动登录...")
            self.login()
        else:
            print("警告: 未提供 client_id/secret 且无有效本地 Token，仅可访问公开接口。")

    def _load_valid_token_from_file(self) -> str:
        if not self.token_path.exists():
            return None
        
        try:
            data = json.loads(self.token_path.read_text(encoding='utf-8'))
            access_token = data.get("accessToken")
            # 统一使用 expiredAt
            expired_at_str = data.get("expiredAt") 
            
            if not access_token or not expired_at_str:
                return None

            # 优化：使用标准库解析 ISO 时间 (支持 Python 3.7+)
            expire_time = datetime.fromisoformat(expired_at_str)
            
            # 获取当前带时区的时间（防止报错：can't subtract offset-naive and offset-aware datetimes）
            # 如果 API 返回的是 UTC 时间，这里会自动处理；如果返回 +08:00，也会自动处理
            now = datetime.now(timezone.utc).astimezone()
            
            # 检查过期 (缓冲 5 分钟)
            if expire_time > now + timedelta(minutes=5): 
                return access_token
            else:
                print(f"本地 Token 已过期 (过期时间: {expired_at_str})")
                return None
                
        except Exception as e:
            print(f"读取 Token 文件失败: {e}")
            return None

    def login(self) -> str:
        if not self.client_id or not self.client_secret:
            raise ValueError("调用 login 需要先配置 client_id 和 client_secret")

        # 获取 Token
        data = self.auth.get_access_token(self.client_id, self.client_secret)
        
        token = data.get("accessToken")
        # API 返回键名为 expiredAt，我们这里也用 expiredAt
        expired_at = data.get("expiredAt")
        
        if not token:
            raise ValueError(f"登录失败：API 返回数据异常: {data}")

        # 更新 Header
        self.header["Authorization"] = f"Bearer {token}"
        
        # 保存到文件
        self._save_token_to_file(token, expired_at)
        
        return token

    def _save_token_to_file(self, token, expired_at):
        try:
            self.token_path.parent.mkdir(parents=True, exist_ok=True)
            
            save_data = {
                "accessToken": token,
                "expiredAt": expired_at, # 保持和 API 一致的键名
                "updated_at": time.time()
            }
            # ensure_ascii=False 保证如果里面有中文路径或者其他字符时可读性更好
            self.token_path.write_text(json.dumps(save_data, indent=2, ensure_ascii=False), encoding='utf-8')
            print(f"Token 已更新并保存至: {self.token_path}")
        except Exception as e:
            print(f"警告: Token 保存文件失败: {e}")
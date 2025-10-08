import requests

from .utils import check_status_code, CloudError


class User:
    def __init__(self, base_url, header):
        self.header = header
        self.base_url = base_url

    def info(self):
        url = self.base_url + "/api/v1/user/info"
        r = requests.get(url, headers=self.header)
        return check_status_code(r)

    def check_token(self):
        url = self.base_url + "/api/v1/user/info"
        r = requests.get(url, headers=self.header)
        try:
            check_status_code(r) # 如果Token无效, 会抛出CloudError异常
        except CloudError:
            return False
        return True # 其他异常不予捕获, 返回上层处理
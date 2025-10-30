class ClientKeyError(Exception):
    def __init__(self, r):
        self.r = r
        super().__init__(f"错误的client_id或client_secret，请检查后重试\n{self.r}")


class AccessTokenError(Exception):
    def __init__(self, r):
        self.r = r
        super().__init__(f"错误的access_token，请检查后重试\n{self.r}")


class CloudError(Exception):
    def __init__(self, r):
        self.r = r
        super().__init__(f"{self.r['message']}")


class PacketLossError(Exception):
    def __init__(self, index: int):
        self.index = index
        super().__init__(f"第{index+1}个分片上传失败，可能是网络问题，请重试")

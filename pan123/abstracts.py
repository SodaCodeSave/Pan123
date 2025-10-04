class Requestable:
    base_url: str
    header: dict

    def __init__(self, base_url: str, header: dict):
        self.base_url = base_url
        self.header = header

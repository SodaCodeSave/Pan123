class Requestable:
    base_url: str
    header: dict

    def __init__(self, base_url: str, header: dict):
        self.base_url = base_url if base_url.endswith("/") else f"{base_url}/"
        self.header = header

    def use_url(self, url: str) -> str:
        return f"{self.base_url}{url[1:] if url.startswith('/') else url}"

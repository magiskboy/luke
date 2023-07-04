import httpx

class FileOpener:
    @classmethod
    def open_from_url(cls, url: str) -> str:
        with httpx.Client() as client:
            response = client.get(url, timeout=10)
            response.raise_for_status()    
            return response.text

    @classmethod
    def open_from_file(cls, filename: str):
        with open(filename, "r") as f:
            return f.read()

    @classmethod
    def open(cls, filename_or_url: str) -> str:
        if filename_or_url.startswith("https://") or filename_or_url.startswith("http://"):
            return cls.open_from_url(filename_or_url)

        return cls.open_from_file(filename_or_url)

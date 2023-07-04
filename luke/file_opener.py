import json
import yaml
import httpx
from .exceptions import OpenFileError


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
        try:
            if filename_or_url.startswith("https://") or filename_or_url.startswith("http://"):
                return cls.open_from_url(filename_or_url)

            return cls.open_from_file(filename_or_url)
        except (httpx.HTTPError, OSError) as e:
            raise OpenFileError() from e

    @classmethod
    def load_from_content(cls, content: str) -> dict:
        try:
            return json.loads(content)
        except json.JSONDecodeError:
            return yaml.load(content, yaml.Loader)

from unittest import mock
import pytest
import httpx
import io
from luke.file_opener import FileOpener
from . import helpers

opener_mocker = mock.Mock(wraps=FileOpener)


CONTENT = """
Person:
    type: object
    properties:
        name:
            type: string
        age:
            type: integer
"""

SCHEMA = {
    "Person": {
        "type": "object",
        "properties": {"name": {"type": "string"}, "age": {"type": "integer"}},
    }
}


@pytest.mark.parametrize(
    ("filename_or_url", "content", "schema"),
    [
        ("http://openapi.org/example.yaml", CONTENT, SCHEMA),
        ("https://openapi.org/example.yaml", CONTENT, SCHEMA),
        ("../schema.yaml", CONTENT, SCHEMA),
    ],
)
def test_open_file(filename_or_url: str, content: str, schema: dict):
    with mock.patch(
        "httpx.Client.get", return_value=httpx.Response(200, text=content, request=httpx.Request(method="GET", url=filename_or_url))
    ), mock.patch("builtins.open", return_value=io.StringIO(content)):
        result = FileOpener.load_from_content(FileOpener.open(filename_or_url))
        helpers.assert_dict(result, schema)

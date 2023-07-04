import logging
from typing import List, Dict, Any, Tuple, Optional
import jsonschema
from .schemas import openapi3_0_schema
from .file_opener import FileOpener
from .resolver import Resolver


logger = logging.getLogger("luke")


class OpenAPISpec:
    def __init__(self):
        self.endpoints: List[Endpoint] = []
        self.spec = dict()

    def load(self, filename_or_url: str):
        spec = self.load_file(filename_or_url)
        self.resolver = Resolver(spec)
        self.validate_openapi(spec)
        self.parse_spec(spec)

    def parse_spec(self, spec: dict):
        self.spec = spec

        for path, endpoints in spec["paths"].items():
            for method, endpoint_spec in endpoints.items():
                try:
                    endpoint = Endpoint(path, method, self)
                    endpoint.load_spec(endpoint_spec)
                    self.endpoints.append(endpoint)
                except (ValueError, KeyError) as e:
                    logger.warn(f"Ignore path {method}:{path} because of {str(e)}")

    @classmethod
    def load_file(cls, filename_or_url: str) -> dict:
        content = FileOpener.open(filename_or_url)

        if not content:
            raise ValueError("File is empty")

        return FileOpener.load_from_content(content)

    @classmethod
    def validate_openapi(cls, spec: dict):
        return jsonschema.validate(spec, openapi3_0_schema)

    def resolve_spec(self, spec: dict) -> dict:
        resolved = spec
        ref = spec.get("$ref")
        if ref:
            resolved = self.resolver.resolve(ref)

        if resolved["type"] == "object":
            if "properties" in resolved:
                for key in resolved["properties"]:
                    resolved["properties"][key] = self.resolve_spec(
                        resolved["properties"][key]
                    )
            else:
                resolved["additionalProperties"] = self.resolve_spec(
                    resolved["additionalProperties"]
                )

        elif resolved["type"] == "array":
            resolved["items"] = self.resolve_spec(resolved["items"])

        return resolved

    @property
    def info(self) -> dict:
        return self.spec["info"]


class Endpoint:
    def __init__(
        self,
        path: str,
        method: str,
        openapi: "OpenAPISpec",
    ):
        self.path = path
        self.method = method
        self.content_specs: Dict[Tuple[str, str], Any] = dict()
        self.headers_spec = {
            "type": "object",
            "properties": dict(),
        }
        self.spec: dict = None  # type: ignore
        self.openapi = openapi

    def load_spec(self, spec: dict):
        self.spec = spec

        content_specs = self.content_specs
        for code, contents in spec["responses"].items():
            if "content" not in contents:
                content_specs[(code, "application/json")] = {"type": "string"}
                continue

            for content_type, content in contents["content"].items():
                try:
                    content_specs[(code, content_type)] = self.openapi.resolve_spec(
                        content["schema"]
                    )
                except KeyError:
                    pass

        headers_spec = self.headers_spec
        if "headers" in spec:
            for header_name, header_spec in spec["headers"].items():
                try:
                    headers_spec["properties"][header_name] = self.openapi.resolve_spec(header_spec["schema"])  # type: ignore
                except KeyError:
                    continue

    def get_content_spec(self, code: str, content_type: str) -> Optional[dict]:
        return self.content_specs.get((code, content_type))

    def get_headers_spec(self) -> dict:
        return self.headers_spec

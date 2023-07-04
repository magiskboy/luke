import logging
from typing import List, Dict, Any, Tuple, Optional
import jsonschema
from .exceptions import ValidateOpenAPIError
from .schemas import openapi3_0_schema
from .file_opener import FileOpener
from .resolver import Resolver


logger = logging.getLogger("luke")


class OpenAPISpec:
    def __init__(self):
        self.endpoints: List[Endpoint] = []
        self.spec = dict()

    def load_and_validate(self, filename_or_url: str):
        file_content = FileOpener.open(filename_or_url)
        if not file_content:
            raise ValueError("File is empty")

        self.spec = FileOpener.load_from_content(file_content)
        self.validate()

    def parse(self):
        self.resolver = Resolver(self.spec)
        self.parse_endpoints()

    def validate(self):
        try:
            return jsonschema.validate(self.spec, openapi3_0_schema)
        except jsonschema.ValidationError as e:
            raise ValidateOpenAPIError() from e

    def parse_endpoints(self):
        for path, endpoint_schemas in self.spec["paths"].items():
            for method, endpoint_schema in endpoint_schemas.items():
                response_schemas = endpoint_schema["responses"]

                # extract schema for contents from response block
                # if document doesn't declare response schema, schema is set to string
                content_specs = {}
                for code, content_schemas in response_schemas.items():
                    if "content" not in content_schemas:
                        content_specs[(code, "application/json")] = {"type": "string"}
                        continue

                    for content_type, content_schema in content_schemas["content"].items():
                        content_specs[(code, content_type)] = self.fulfill_schema(
                            content_schema["schema"]
                        )

                # extract schema for headers from response block
                header_specs = {
                    "type": "object",
                    "properties": {},
                }
                if "headers" in response_schemas:
                    for header_name, header_spec in response_schemas["headers"].items():
                        header_specs["properties"][header_name] = self.fulfill_schema(header_spec["schema"])  # type: ignore

                self.endpoints.append(Endpoint(path, method, content_specs, header_specs))
                    

    def fulfill_schema(self, spec: dict) -> dict:
        ref = spec.get("$ref")
        if ref:
            spec = self.resolver.resolve(ref)

        if spec["type"] == "object":
            if "properties" in spec:
                for key in spec["properties"]:
                    spec["properties"][key] = self.fulfill_schema(
                        spec["properties"][key]
                    )
            else:
                spec["additionalProperties"] = self.fulfill_schema(
                    spec["additionalProperties"]
                )

        elif spec["type"] == "array":
            spec["items"] = self.fulfill_schema(spec["items"])

        return spec

    @property
    def info(self) -> dict:
        return self.spec["info"]


class Endpoint:
    def __init__(
        self,
        path: str,
        method: str,
        content_specs: Dict[Tuple[str, str], Any] = None, # type: ignore
        header_specs: Dict = None,  # type: ignore
    ):
        self.path = path
        self.method = method
        self.content_specs: Dict[Tuple[str, str], Any] = content_specs
        self.header_specs = header_specs

    def get_content_spec(self, code: str, content_type: str) -> Optional[dict]:
        return self.content_specs.get((code, content_type))

    def get_header_specs(self) -> dict:
        return self.header_specs

    def __str__(self):
        return f"<Endpoint {self.method} {self.path}>"

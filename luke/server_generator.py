from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from .openapi import OpenAPISpec, Endpoint
from .data_generators import Generator


class ServerGenerator:
    def __init__(self, spec: OpenAPISpec):
        self._spec = spec

    def make_server(self) -> FastAPI:
        spec = self._spec

        info = spec.info

        app = FastAPI(
            title=info.get("title", "Luke Mock Server"),
            version=info.get("version", "1.0.0"),
        )

        for endpoint in spec.endpoints:
            handler = self.make_endpoint_handler(endpoint)
            app.add_api_route(endpoint.path, handler, methods=[endpoint.method])

        return app

    def make_endpoint_handler(self, spec: Endpoint):
        def handler(request: Request):
            expected_status = request.headers.get("x-luke-expected-status", "200")
            expected_content_type = request.headers.get("accept", "application/json")

            content_spec = spec.get_content_spec(expected_status, expected_content_type)
            if not content_spec:
                return JSONResponse({"message": "Can not specification for this mock", "from": "luke"}, 400)

            content = Generator().gen_data(content_spec)

            headers = Generator().gen_data(spec.get_headers_spec())
            for k in headers:
                headers[k] = str(headers[k])

            return JSONResponse(content, int(expected_status), headers)

        return handler

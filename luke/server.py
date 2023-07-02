from typing import Callable
from copy import deepcopy
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import JSONResponse, HTMLResponse
from starlette.schemas import SchemaGenerator
from .openapi import OpenAPISpec, Endpoint
from .generators import Generator


class ServerGenerator:
    def make_server(self, spec: OpenAPISpec) -> Callable:
        app = Starlette()
        openapi_spec = deepcopy(spec.spec)
        openapi_spec["servers"].append({"url": "http://localhost:8000"})
        schema_generator = SchemaGenerator(openapi_spec)
        app.add_route("/spec", lambda request: schema_generator.OpenAPIResponse(request))
        async def swagger(request: Request):
            content = """
                <html lang="en">
                    <head>
                        <link rel="stylesheet" href="https://unpkg.com/swagger-ui-dist@4.5.0/swagger-ui.css" />
                    </head>
                    <div id="swagger-ui"></div>
                    <script src="https://unpkg.com/swagger-ui-dist@4.5.0/swagger-ui-bundle.js"></script>
                    <script>
                      window.onload = () => {
                        window.ui = SwaggerUIBundle({
                          url: '/spec',
                          dom_id: '#swagger-ui',
                        });
                      };
                    </script>
                </html>"""
            return HTMLResponse(content)
        app.add_route("/docs", swagger)

        for endpoint in spec.endpoints:
            handler = self.make_endpoint_handler(endpoint)
            app.add_route(endpoint.path, handler, methods=[endpoint.method])

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

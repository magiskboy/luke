try:
    from typing import Annotated            # type: ignore
except ImportError:
    from typing_extensions import Annotated # type: ignore

import uvicorn
import typer
from .server_generator import ServerGenerator
from .openapi import OpenAPISpec


cli = typer.Typer(name="luke")

@cli.command("start")
def start_server(
    spec_file: Annotated[typer.FileText, typer.Argument()],
    host: str = typer.Option(default="127.0.0.1"),
    port: int = typer.Option(default=8000),
):
    spec = OpenAPISpec()
    spec.load_from_file(spec_file)
    generator = ServerGenerator(spec)
    server = generator.make_server()
    uvicorn.run(server, log_level="info")

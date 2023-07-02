import enum
import uvicorn
import typer
from jsonschema import ValidationError
from .server import ServerGenerator
from .openapi import OpenAPISpec


cli = typer.Typer(name="luke", no_args_is_help=True, pretty_exceptions_enable=False)


class LogLevel(str, enum.Enum):
    info = "info"
    critical = "critical"
    debug = "debug"
    warn = "warn"
    noset = "noset"


@cli.command("mock")
def start_server(
    file: str = typer.Argument(help="Filename or URL of specification"),
    host: str = typer.Option(default="127.0.0.1"),
    port: int = typer.Option(default=8000),
    log_level: LogLevel = typer.Option(default=LogLevel.info),
):
    spec = OpenAPISpec()
    spec.load(file)
    generator = ServerGenerator()
    server = generator.make_server(spec)
    uvicorn.run(server, log_level=log_level, host=host, port=port)


@cli.command("validate")
def validate_apidoc(
    file: str = typer.Argument(help="Filename or URL of specification"),
):
    try:
        spec = OpenAPISpec.load_file(file)
    except Exception:
        typer.echo(typer.style(f"Can't open file at {file}, please check it", fg="red"))
        exit(1)
    
    try:
        OpenAPISpec.validate_openapi(spec)
    except ValidationError as e:
        typer.echo(typer.style("Validate failed!!!", fg="red"))
        typer.echo(typer.style(e.message, fg="red", bold=True))
        exit(1)

    typer.echo(typer.style("Validate pass!!!", fg="green"))


@cli.command("bundle")
def bundle_apidoc():
    typer.echo("In planning...")

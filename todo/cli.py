from typing import Optional
import typer
from todo import __app_name__, __version__, config, ERRORS
from pathlib import Path

app = typer.Typer()

def _version_callback(value: bool) -> None:
    if value:
        typer.echo(f"{__app_name__} v{__version__}")
        raise typer.Exit(0)
    
@app.callback()
def main(
    version: Optional[bool] = typer.Option(
        None, "--version", '-v', help='Show the ap version no. & exit', callback=_version_callback, is_eager=True
    )
) -> None:
    return


@app.command()
def init(db_path: str = typer.Option(
        str(config.DEFAULT_DB_FILE_PATH),
        "--db-path",
        "-db"
    )) -> None:
    """Initialize the to-do database."""
    app_init_error = config.init_app(db_path)

    if app_init_error:
        typer.secho(
            f'Creating config file failed with "{ERRORS[app_init_error]}"',
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)
    
    db_init_error = config.init_database(Path(db_path))

    if db_init_error:
        typer.secho(
            f'Creating database failed with "{ERRORS[db_init_error]}"',
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)
    else:
        typer.secho(f"The to-do database location is: '{db_path}' ", fg=typer.colors.GREEN)



# def get_todoer() -> rptodo.Todoer:
#     if config.CONFIG_FILE_PATH.exists():
#         db_path = config.get_database_path(config.CONFIG_FILE_PATH)
#     else:
#         typer.secho(
#             'Config file not found. Please, run "todo init"',
#             fg=typer.colors.RED,
#         )
#         raise typer.Exit(1)
#     if db_path.exists():
#         return rptodo.Todoer(db_path)
#     else:
#         typer.secho(
#             'Database not found. Please, run "rptodo init"',
#             fg=typer.colors.RED,
#         )
#         raise typer.Exit(1)



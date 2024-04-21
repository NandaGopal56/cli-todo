from typing import Optional, List
import typer
from todo import __app_name__, __version__, config, ERRORS, model
from pathlib import Path
import os

app = typer.Typer()
    
def version_callback(value: bool) -> None:
    if value:
        typer.echo(f"{__app_name__} v{__version__}")
        raise typer.Exit()

def author_callback(value: bool) -> None:
    if value:
        typer.echo("Author: Nanda Gopal Pattanayk")
        raise typer.Exit()
    
@app.callback()
def main(
    version: bool = typer.Option(None, "--version", "-v", help="Show version", callback=version_callback, is_eager=True),
    author: bool = typer.Option(None, "--author", "-a", help="Show author", callback=author_callback, is_eager=True),
) -> None:
    pass




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


def get_to_manager() -> model.TodoManager:
    if config.CONFIG_FILE_PATH.exists():
        db_path = config.get_database_path()
    else:
        typer.secho(
            'Config file not found. Please, run "todo init"',
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)
    if os.path.exists(db_path):
        # todo: make this dynamic as per config file
        storage_type = model.JSONStorage()
        return model.TodoManager(storage_type)
    else:
        typer.secho(
            'Database not found. Please, run "rptodo init"',
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)

#todo: fix id auto increment while printing but not in storage layer
def print_formatted_todo_in_cli(todos: List[model.TodoItem]) -> None:
    """Print the To-do item in formatted tabular format in terminal"""
    columns = (
        "ID.  ",
        "| Priority  ",
        "| Status  ",
        "| Description  ",
    )
    headers = "".join(columns)
    typer.secho(headers, fg=typer.colors.BLUE, bold=True)
    typer.secho("-" * len(headers), fg=typer.colors.BLUE)
    for id, todo in enumerate(todos, 1):
        desc, priority, done = todo.description, todo.priority.name, todo.status.name
        typer.secho(
            f"{id}{(len(columns[0]) - len(str(id))) * ' '}"
            f"| ({priority}){(len(columns[1]) - len(str(priority)) - 4) * ' '}"
            f"| {done}{(len(columns[2]) - len(str(done)) - 2) * ' '}"
            f"| {desc}",
            fg=typer.colors.BLUE,
        )
    typer.secho("-" * len(headers) + "\n", fg=typer.colors.BLUE)


@app.command(name='add')
def add(
    description: str,
    priority: model.Priority = typer.Option(model.Priority.low, "--priority", "-p", help="Priority level (low, medium, high)"),
    status: model.Status = typer.Option(model.Status.pending, "--status", "-s", help="Status (pending, completed)")
) -> None:
    """Add a new to-do with a DESCRIPTION."""
    todoer = get_to_manager()
    todo_item, status = todoer.create_todo(description, priority, status)
    if status != 0:
        typer.secho(
            f'Adding to-do failed with "{status}"', fg=typer.colors.RED
        )
        raise typer.Exit(1)
    else:
        typer.secho("\nBelow to-do was added :\n", fg=typer.colors.BLUE, bold=True)
        print_formatted_todo_in_cli([todo_item])

@app.command(name='list')
def list_all_todos() -> None:
    todo_manager = get_to_manager()
    todos = todo_manager.list_todos()

    if len(todos) == 0:
        typer.secho(
            "There are no tasks in the to-do list yet", fg=typer.colors.RED
        )
        raise typer.Exit()
    typer.secho("\nto-do list:\n", fg=typer.colors.BLUE, bold=True)
    print_formatted_todo_in_cli(todos)



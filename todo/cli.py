from typing import Optional, List
import typer
from todo import __app_name__, __version__, config, ERRORS, model
from pathlib import Path

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
    for todo in todos:
        id, desc, priority, done = todo.id, todo.description, todo.priority.name, todo.status.name
        typer.secho(
            f"{id}{(len(columns[0]) - len(str(id))) * ' '}"
            f"| {priority}{(len(columns[1]) - len(str(priority)) - 4) * ' '}"
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
    todoer = model.get_todo_manager()
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
def list_todos(
    todo_id: int = typer.Argument(default=None, help="Enter todo_id to get list only one todo")
) -> None:
    """List available To-Dos"""
    todo_manager = model.get_todo_manager()
    if todo_id:
        try:
            todos = [todo_manager.get_todo_by_id(todo_id)]
        except ValueError as e:
            typer.secho(
                e, fg=typer.colors.RED
            )
            raise typer.Exit()
    else:
        todos = todo_manager.list_todos()
        if len(todos) == 0:
            typer.secho(
                "There are no tasks in the to-do list yet", fg=typer.colors.RED
            )
            raise typer.Exit()
        
    typer.secho("\nto-do list:\n", fg=typer.colors.BLUE, bold=True)
    print_formatted_todo_in_cli(todos)


@app.command(name='remove')
def remove(
    todo_id: int = typer.Argument(help="Enter todo_id to which needs to be removed")
) -> None:
    """remove todo with given todo_id if available"""
    todo_manager = model.get_todo_manager()
    try:
        todo_item = [todo_manager.get_todo_by_id(todo_id)]
        todo_manager.delete_todo(todo_id)
        typer.secho(
                f"Below Todo with id {todo_id} is deleted. \n", fg=typer.colors.RED, bold=True
            )
        print_formatted_todo_in_cli(todo_item)
        raise typer.Exit()
    except ValueError as e:
        typer.secho(
            e, fg=typer.colors.RED
        )
        raise typer.Exit()
    

@app.command(name='update')
def update(
    todo_id: int = typer.Argument(help="Enter todo_id to which needs to be removed"),
    description: str = typer.Option(None, "--description", "-d", help="update description"),
    status: model.Status = typer.Option(None, "--status", "-s", help="Update Status (pending, completed)"),
    priority: model.Priority = typer.Option(None, "--priority", "-p", help="Update Priority level (low, medium, high)")
) -> None:
    """Update a given todo with the new data provided"""
    todo_manager = model.get_todo_manager()
    try:
        todo_item = [todo_manager.get_todo_by_id(todo_id)]
        
        if all(v is None for v in [description, status, priority]):
            typer.secho('Atleast one of the property between Description or Status or Priority needs to be given in order to update the todo', fg=typer.colors.RED)
            raise typer.Exit()

        todo_item = todo_manager.update_todo(todo_id=todo_id, description=description, priority=priority, status=status)
        typer.secho(
                f"Todo with id {todo_id} is updated as below. \n", fg=typer.colors.BLUE, bold=True
            )
        print_formatted_todo_in_cli([todo_item])

    except ValueError as e:
        typer.secho(
            e, fg=typer.colors.RED
        )
        raise typer.Exit()
    




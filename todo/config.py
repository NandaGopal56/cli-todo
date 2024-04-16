import json
from pathlib import Path

import typer

from todo import (
    DB_WRITE_ERROR, DIRECTORY_ERROR, FILE_ERROR, SUCCESS, __app_name__
)

CONFIG_DIR_PATH = Path(typer.get_app_dir(__app_name__))
CONFIG_FILE_PATH = CONFIG_DIR_PATH / "config.json"
DEFAULT_DB_FILE_PATH = CONFIG_DIR_PATH / "datastore_todo.json"

def init_app(db_path: str) -> int:
    """Initialize the application."""
    config_code = _init_config_file()
    if config_code != SUCCESS:
        return config_code
    
    json_datastore_code = _create_json_datastore(db_path)
    if json_datastore_code != SUCCESS:
        return json_datastore_code
    
    return SUCCESS


def _init_config_file() -> int:
    try:
        CONFIG_DIR_PATH.mkdir(exist_ok=True)
    except OSError:
        return DIRECTORY_ERROR
    try:
        CONFIG_FILE_PATH.touch(exist_ok=True)
        with open(CONFIG_FILE_PATH, "w") as json_file:
            json.dump({'app': __app_name__}, json_file)
    except OSError:
        return FILE_ERROR
    return SUCCESS

def _create_json_datastore(json_datastore_path: str) -> int:
    try:
        # Read existing content or initialize as empty dictionary
        try:
            with open(CONFIG_FILE_PATH, "r") as json_file:
                config_json = json.load(json_file)
        except json.JSONDecodeError:
            config_json = {}
        
        # Update or add new key-value pair
        config_json["json_datastore"] = str(json_datastore_path)

        # Write updated content back to the file
        with open(CONFIG_FILE_PATH, "w") as json_file:
            json.dump(config_json, json_file)
    except OSError:
        return DB_WRITE_ERROR
    return SUCCESS

# def get_database_path(config_file: Path) -> Path:
#     """Return the current path to the to-do database."""
#     config_parser = configparser.ConfigParser()
#     config_parser.read(config_file)
#     return Path(config_parser["General"]["database"])

def init_database(db_path: Path) -> int:
    """Create the to-do database."""
    try:
        db_path.write_text("[]")  # Empty to-do list
        return SUCCESS
    except OSError:
        return DB_WRITE_ERROR
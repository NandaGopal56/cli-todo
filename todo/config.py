import json
from pathlib import Path
from enum import Enum
import typer
from typing import Tuple

from todo import (
    DB_READ_ERROR, DB_WRITE_ERROR, DIRECTORY_ERROR, FILE_ERROR, SUCCESS, __app_name__
)

class StorageTypes(str, Enum):
    json = 'json'
    in_memory = 'in_memory'

APP_WORKING_DIRRECTORY = Path(typer.get_app_dir(__app_name__))
CONFIG_FILE_PATH = APP_WORKING_DIRRECTORY / "config.json"
DEFAULT_DB_FILE_PATH = APP_WORKING_DIRRECTORY / "todos.json"

def init_app(db_path: str, storage: StorageTypes) -> int:
    """Initialize the application."""
    config_code = _init_config_file(storage)
    if config_code != SUCCESS:
        return config_code
    
    json_datastore_code = _create_json_datastore(db_path)
    if json_datastore_code != SUCCESS:
        return json_datastore_code
    
    return SUCCESS


def _init_config_file(storage: StorageTypes) -> int:
    try:
        APP_WORKING_DIRRECTORY.mkdir(exist_ok=True)
    except OSError:
        return DIRECTORY_ERROR
    try:
        CONFIG_FILE_PATH.touch(exist_ok=True)
        with open(CONFIG_FILE_PATH, "w") as json_file:
            json.dump({'app': __app_name__, 'storage_type': storage.name}, json_file)
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

def get_database_path() -> Tuple[StorageTypes, Path]:
    """Return the current path to the to-do database."""
    try:
        with open(CONFIG_FILE_PATH, "r") as json_file:
            config_json = json.load(json_file)
    except OSError:
        return DB_READ_ERROR
    return config_json['storage_type'], config_json['json_datastore']

def init_database(db_path: Path) -> int:
    """Create the to-do database."""
    try:
        db_path.write_text("[]")  # Empty to-do list
        return SUCCESS
    except OSError:
        return DB_WRITE_ERROR
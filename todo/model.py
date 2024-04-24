import json
from pathlib import Path
from typing import Any, Dict, List, NamedTuple, Optional, Literal
from todo import DB_READ_ERROR, DB_WRITE_ERROR, JSON_ERROR, SUCCESS
from abc import ABC, abstractmethod
from pydantic import BaseModel, Field
from todo import config
from enum import Enum
import typer, os

class Priority(str, Enum):
    high = 'high'
    medium = 'medium'
    low = 'low'

class Status(str, Enum):
    completed = 'completed'
    pending = 'pending'

class TodoItem(BaseModel):
    id: Optional[int] = Field(default_factory=lambda: max((todo.id for todo in get_todo_manager().list_todos()), default=0) + 1)
    description: str
    priority: Priority
    status: Status

# Abstract DataStore interface
class StorageInterface(ABC):
    
    @abstractmethod
    def create_todo(self, todo: TodoItem) -> TodoItem:
        pass

    @abstractmethod
    def get_todo_by_id(self, todo_id: int) -> TodoItem:
        pass

    @abstractmethod
    def update_todo(self, todo: TodoItem) -> TodoItem:
        pass

    @abstractmethod
    def delete_todo(self, todo_id: int) -> None:
        pass

    @abstractmethod
    def list_todos(self) -> List[TodoItem]:
        pass



class JSONStorage(StorageInterface):

    def __init__(self):
        _, self.filename = config.get_database_path()
        try:
            with open(self.filename, 'r') as file:
                self.data = json.load(file)
        except FileNotFoundError:
            self.data = []

    def _save_data(self):
        with open(self.filename, 'w') as file:
            json.dump(self.data, file)

    def create_todo(self, todo: TodoItem) -> TodoItem:
        try:
            todo_dict = todo.model_dump()
            self.data.append(todo_dict)
            self._save_data()
            return TodoItem(**todo_dict), SUCCESS
        except Exception as e:
            return None, DB_WRITE_ERROR

    def get_todo_by_id(self, todo_id: int) -> TodoItem:
        for todo in self.data:
            if todo['id'] == todo_id:
                return TodoItem(**todo)
        raise ValueError(f"Todo with id {todo_id} not found")

    def update_todo(self, todo: TodoItem) -> TodoItem:
        for index, stored_todo in enumerate(self.data):
            if stored_todo['id'] == todo.id:
                self.data[index] = todo.model_dump()
                self._save_data()
                return todo
        raise ValueError(f"Todo with id {todo.id} not found")

    def delete_todo(self, todo_id: int) -> None:
        self.data = [todo for todo in self.data if todo['id'] != todo_id]
        self._save_data()

    def list_todos(self) -> List[TodoItem]:
        return [TodoItem(**todo) for todo in self.data]
        

class InMemoryStorage(StorageInterface):

    def __init__(self):
        self.data = []

    def create_todo(self, todo: TodoItem) -> TodoItem:
        try:
            todo.id = len(self.data) + 1
            self.data.append(todo)
            return todo, SUCCESS
        except Exception as e:
            return None, DB_WRITE_ERROR

    def get_todo_by_id(self, todo_id: int) -> TodoItem:
        for todo in self.data:
            if todo.id == todo_id:
                return todo
        raise ValueError(f"Todo with id {todo_id} not found")

    def update_todo(self, todo: TodoItem) -> TodoItem:
        for index, stored_todo in enumerate(self.data):
            if stored_todo.id == todo.id:
                self.data[index] = todo
                return todo
        raise ValueError(f"Todo with id {todo.id} not found")

    def delete_todo(self, todo_id: int) -> None:
        self.data = [todo for todo in self.data if todo.id != todo_id]

    def list_todos(self) -> List[TodoItem]:
        return self.data


class TodoManager:

    def __init__(self, storage):
        self.storage = storage

    def create_todo(self, description: str, priority: str, status: str) -> TodoItem:
        todo = TodoItem(description=description, priority=priority, status=status)
        return self.storage.create_todo(todo)

    def get_todo_by_id(self, todo_id: int) -> TodoItem:
        return self.storage.get_todo_by_id(todo_id)

    def update_todo(self, todo_id: int, description: str = None, priority: str = None, status: str = None) -> TodoItem:
        todo = self.get_todo_by_id(todo_id)
    
        if description:
            todo.description = description
        if priority:
            todo.priority = priority
        if status:
            todo.status = status
        
        return self.storage.update_todo(todo)

    def delete_todo(self, todo_id: int) -> None:
        return self.storage.delete_todo(todo_id)

    def list_todos(self) -> List[TodoItem]:
        return self.storage.list_todos()
    

def get_todo_manager() -> TodoManager:
    if config.CONFIG_FILE_PATH.exists():
        storage_type, db_path = config.get_database_path()
    else:
        typer.secho(
            'Config file not found. Please, run "todo init"',
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)
    if os.path.exists(db_path):
        if storage_type == config.StorageTypes.in_memory.name:
            storage_type = InMemoryStorage()
        else:
            storage_type = JSONStorage()

        return TodoManager(storage_type)
    else:
        typer.secho(
            'Database not found. Please, run "rptodo init"',
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)
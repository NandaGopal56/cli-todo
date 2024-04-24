import pytest
from todo.model import InMemoryStorage, TodoManager, JSONStorage, Status, Priority

@pytest.fixture
def in_memory_manager():
    storage = InMemoryStorage()
    return TodoManager(storage)

@pytest.fixture
def json_manager():
    storage = JSONStorage()
    return TodoManager(storage)


def test_integration_create_and_get_todo(in_memory_manager, json_manager):
    for manager in [in_memory_manager, json_manager]:
        created_todo, status = manager.create_todo("Test Description", Priority.low, Status.pending)
        assert status == 0

        retrieved_todo = manager.get_todo_by_id(created_todo.id)
        assert retrieved_todo == created_todo

def test_integration_update_todo(in_memory_manager, json_manager):
    for manager in [in_memory_manager, json_manager]:
        created_todo, status = manager.create_todo("Test Description", Priority.low, Status.pending)
        result = manager.update_todo(1, "new descriptiond", Priority.high, Status.completed)
        
        retrieved_todo = manager.get_todo_by_id(1)
        assert result == retrieved_todo


def test_integration_delete_todo(in_memory_manager, json_manager):
    for manager in [in_memory_manager, json_manager]:
        result = manager.delete_todo(0)
        assert result == None

        with pytest.raises(ValueError) as exc_info:
            manager.get_todo_by_id(0)
        
        assert str(exc_info.value) == f"Todo with id {0} not found"



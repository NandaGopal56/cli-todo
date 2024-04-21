import pytest
from todo.model import InMemoryStorage, TodoManager

@pytest.fixture
def in_memory_manager():
    storage = InMemoryStorage()
    return TodoManager(storage)


def test_integration_create_and_get_todo_in_memory(in_memory_manager):
    created_todo = in_memory_manager.create_todo("Test", "Test Description", "High", "Pending")
    retrieved_todo = in_memory_manager.get_todo_by_id(created_todo.id)
    assert retrieved_todo == created_todo

def test_integration_delete_todo_in_memory(in_memory_manager):
    result = in_memory_manager.delete_todo(0)
    assert result == None

    with pytest.raises(ValueError) as exc_info:
        in_memory_manager.get_todo_by_id(0)
    
    assert str(exc_info.value) == f"Todo with id {0} not found"
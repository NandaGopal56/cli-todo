import pytest
from todo.model import JSONStorage, TodoManager

@pytest.fixture
def json_manager(tmp_path):
    # filename = tmp_path / "test.json"
    storage = JSONStorage()
    return TodoManager(storage)


def test_integration_create_and_get_todo_json(json_manager):
    created_todo = json_manager.create_todo("Test", "Test Description", "High", "Pending")
    retrieved_todo = json_manager.get_todo_by_id(created_todo.id)
    assert retrieved_todo == created_todo

def test_integration_delete_todo_in_memory(json_manager):
    result = json_manager.delete_todo(0)
    assert result == None

    with pytest.raises(ValueError) as exc_info:
        json_manager.get_todo_by_id(0)
    
    assert str(exc_info.value) == f"Todo with id {0} not found"


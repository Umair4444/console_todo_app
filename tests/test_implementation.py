"""
Simple test to verify the functionality of the todo application.
"""
import sys
import os
import tempfile
import json

# Add the project root to the Python path
project_root = os.path.abspath('.')
sys.path.insert(0, project_root)

# Now import the modules directly
from src.models.todo_item import TodoItem
from src.storage.file_storage import FileStorage
from src.services.todo_service import TodoService
from src.utils.validation import validate_task_description


def test_todo_item():
    """Test the TodoItem model."""
    print("Testing TodoItem model...")
    
    # Test creating a valid TodoItem
    item = TodoItem(id=1, description="Test task")
    assert item.id == 1
    assert item.description == "Test task"
    assert item.completed is False
    print("✓ TodoItem creation works")
    
    # Test validation
    assert validate_task_description("Valid description")
    assert not validate_task_description("")
    assert not validate_task_description("   ")
    print("✓ Validation works")
    
    # Test updating description
    item.update_description("Updated task")
    assert item.description == "Updated task"
    print("✓ TodoItem update works")


def test_file_storage():
    """Test the FileStorage functionality."""
    print("\nTesting FileStorage...")
    
    # Create a temporary file for testing
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as temp_file:
        temp_path = temp_file.name
    
    try:
        # Create FileStorage instance
        storage = FileStorage(temp_path)
        
        # Test saving and loading tasks
        test_tasks = [
            {
                "id": 1,
                "description": "Test task 1",
                "completed": False,
                "created_at": "2025-12-30T10:00:00",
                "updated_at": "2025-12-30T10:00:00"
            },
            {
                "id": 2,
                "description": "Test task 2", 
                "completed": True,
                "created_at": "2025-12-30T11:00:00",
                "updated_at": "2025-12-30T11:00:00"
            }
        ]
        
        storage.save_tasks(test_tasks)
        loaded_tasks = storage.load_tasks()
        
        assert len(loaded_tasks) == 2
        assert loaded_tasks[0]["description"] == "Test task 1"
        assert loaded_tasks[1]["completed"] is True
        print("✓ FileStorage save/load works")
    finally:
        # Clean up
        if os.path.exists(temp_path):
            os.remove(temp_path)


def test_todo_service():
    """Test the TodoService functionality."""
    print("\nTesting TodoService...")
    
    # Create a temporary file for testing
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as temp_file:
        temp_path = temp_file.name
    
    try:
        # Create TodoService instance
        storage = FileStorage(temp_path)
        service = TodoService(storage=storage)
        
        # Test adding a task
        task = service.add_task("Test task for service")
        assert task.id == 1
        assert task.description == "Test task for service"
        print("✓ TodoService add_task works")
        
        # Test getting all tasks
        tasks = service.get_all_tasks()
        assert len(tasks) == 1
        assert tasks[0].description == "Test task for service"
        print("✓ TodoService get_all_tasks works")
        
        # Test updating a task
        updated_task = service.update_task(1, "Updated test task")
        assert updated_task.description == "Updated test task"
        print("✓ TodoService update_task works")
        
        # Test marking as complete
        completed_task = service.mark_task_complete(1)
        assert completed_task.completed is True
        print("✓ TodoService mark_task_complete works")
        
        # Test deleting a task
        deleted_task = service.delete_task(1)
        assert deleted_task.id == 1
        tasks = service.get_all_tasks()
        assert len(tasks) == 0
        print("✓ TodoService delete_task works")
    finally:
        # Clean up
        if os.path.exists(temp_path):
            os.remove(temp_path)


if __name__ == "__main__":
    print("Running basic functionality tests...\n")
    
    test_todo_item()
    test_file_storage()
    test_todo_service()
    
    print("\n✓ All tests passed! The implementation is working correctly.")
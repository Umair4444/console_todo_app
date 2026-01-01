"""
Pytest configuration and fixtures for the todo application.
"""
import pytest
import tempfile
import os
import sys
from pathlib import Path

# Add the project root to the Python path
project_root = os.path.join(os.path.dirname(__file__), '..')
sys.path.insert(0, project_root)

from src.storage.file_storage import FileStorage
from src.services.todo_service import TodoService


@pytest.fixture
def temp_file():
    """
    Create a temporary file for testing.
    
    Yields:
        Path to the temporary file
    """
    with tempfile.NamedTemporaryFile(delete=False, suffix='.json') as tmp:
        tmp_path = Path(tmp.name)
    yield tmp_path
    # Cleanup after test
    if tmp_path.exists():
        os.remove(tmp_path)


@pytest.fixture
def empty_storage(temp_file):
    """
    Create an empty FileStorage instance for testing.
    
    Args:
        temp_file: Temporary file path from fixture
        
    Yields:
        FileStorage instance
    """
    storage = FileStorage(str(temp_file))
    yield storage
    # Cleanup happens in temp_file fixture


@pytest.fixture
def sample_tasks():
    """
    Provide sample tasks for testing.
    
    Yields:
        List of sample task dictionaries
    """
    tasks = [
        {
            "id": 1,
            "description": "Buy groceries",
            "completed": False,
            "created_at": "2025-12-30T10:00:00",
            "updated_at": "2025-12-30T10:00:00"
        },
        {
            "id": 2,
            "description": "Finish report",
            "completed": True,
            "created_at": "2025-12-30T09:30:00",
            "updated_at": "2025-12-30T11:15:00"
        }
    ]
    yield tasks


@pytest.fixture
def todo_service_with_tasks(empty_storage, sample_tasks):
    """
    Create a TodoService with sample tasks for testing.
    
    Args:
        empty_storage: Empty FileStorage instance
        sample_tasks: Sample tasks to populate the storage
        
    Yields:
        TodoService instance with sample tasks
    """
    # Save sample tasks to storage
    empty_storage.save_tasks(sample_tasks)
    
    # Create and return TodoService
    service = TodoService(storage=empty_storage)
    yield service
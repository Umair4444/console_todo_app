"""
Unit tests for atomic write operations in file storage.
"""
import pytest
import tempfile
import os
from pathlib import Path
from src.storage.file_storage import FileStorage
from src.utils.file_utils import atomic_write, atomic_write_bytes


class TestAtomicWriteOperations:
    """Unit tests for atomic write operations."""
    
    def test_atomic_write_creates_file_with_content(self, temp_file):
        """Test that atomic_write creates a file with the specified content."""
        test_content = "This is test content"
        
        # Use atomic_write to write content
        atomic_write(temp_file, test_content)
        
        # Verify the file was created with correct content
        assert temp_file.exists()
        with open(temp_file, 'r', encoding='utf-8') as f:
            content = f.read()
        assert content == test_content
    
    def test_atomic_write_creates_directories_if_needed(self):
        """Test that atomic_write creates directories if they don't exist."""
        with tempfile.TemporaryDirectory() as temp_dir:
            nested_path = Path(temp_dir) / "subdir" / "nested" / "test.txt"
            test_content = "This is test content"
            
            # Use atomic_write to write content to nested path
            atomic_write(nested_path, test_content)
            
            # Verify the file and directories were created with correct content
            assert nested_path.exists()
            with open(nested_path, 'r', encoding='utf-8') as f:
                content = f.read()
            assert content == test_content
    
    def test_atomic_write_overwrites_existing_file(self, temp_file):
        """Test that atomic_write overwrites existing file content."""
        initial_content = "Initial content"
        new_content = "New content"
        
        # Write initial content
        with open(temp_file, 'w', encoding='utf-8') as f:
            f.write(initial_content)
        
        # Use atomic_write to overwrite
        atomic_write(temp_file, new_content)
        
        # Verify the file has new content
        with open(temp_file, 'r', encoding='utf-8') as f:
            content = f.read()
        assert content == new_content
    
    def test_atomic_write_bytes_creates_file_with_content(self):
        """Test that atomic_write_bytes creates a file with the specified binary content."""
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_path = Path(temp_file.name)
        
        try:
            test_content = b"This is test binary content"
            
            # Use atomic_write_bytes to write content
            atomic_write_bytes(temp_path, test_content)
            
            # Verify the file was created with correct content
            assert temp_path.exists()
            with open(temp_path, 'rb') as f:
                content = f.read()
            assert content == test_content
        finally:
            # Clean up
            if temp_path.exists():
                os.remove(temp_path)
    
    def test_atomic_write_bytes_creates_directories_if_needed(self):
        """Test that atomic_write_bytes creates directories if they don't exist."""
        with tempfile.TemporaryDirectory() as temp_dir:
            nested_path = Path(temp_dir) / "subdir" / "nested" / "test.bin"
            test_content = b"This is test binary content"
            
            # Use atomic_write_bytes to write content to nested path
            atomic_write_bytes(nested_path, test_content)
            
            # Verify the file and directories were created with correct content
            assert nested_path.exists()
            with open(nested_path, 'rb') as f:
                content = f.read()
            assert content == test_content
    
    def test_file_storage_uses_atomic_write_operations(self, temp_file):
        """Test that FileStorage uses atomic write operations for data integrity."""
        # Create initial tasks
        initial_tasks = [
            {
                "id": 1,
                "description": "Initial task",
                "completed": False,
                "created_at": "2025-12-30T10:00:00",
                "updated_at": "2025-12-30T10:00:00"
            }
        ]
        
        # Create FileStorage and save initial tasks
        storage = FileStorage(str(temp_file))
        storage.save_tasks(initial_tasks)
        
        # Verify the tasks were saved
        loaded_tasks = storage.load_tasks()
        assert len(loaded_tasks) == 1
        assert loaded_tasks[0]["description"] == "Initial task"
        
        # Add more tasks
        additional_tasks = [
            {
                "id": 1,
                "description": "Initial task",
                "completed": False,
                "created_at": "2025-12-30T10:00:00",
                "updated_at": "2025-12-30T10:00:00"
            },
            {
                "id": 2,
                "description": "Additional task",
                "completed": True,
                "created_at": "2025-12-30T11:00:00",
                "updated_at": "2025-12-30T11:00:00"
            }
        ]
        
        # Save updated tasks
        storage.save_tasks(additional_tasks)
        
        # Verify the updated tasks were saved correctly
        loaded_tasks = storage.load_tasks()
        assert len(loaded_tasks) == 2
        assert loaded_tasks[1]["description"] == "Additional task"
        assert loaded_tasks[1]["completed"] is True
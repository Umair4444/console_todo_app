"""
Unit tests for TodoItem model.
"""
import pytest
from datetime import datetime
from src.models.todo_item import TodoItem
from src.utils.handlers import InvalidTaskDescriptionError


class TestTodoItem:
    """Tests for the TodoItem model."""
    
    def test_create_valid_todo_item(self):
        """Test creating a valid TodoItem."""
        item = TodoItem(id=1, description="Test task")
        
        assert item.id == 1
        assert item.description == "Test task"
        assert item.completed is False
        assert item.created_at is not None
        assert item.updated_at is not None
    
    def test_create_todo_item_with_empty_description_fails(self):
        """Test that creating a TodoItem with empty description raises an error."""
        with pytest.raises(InvalidTaskDescriptionError):
            TodoItem(id=1, description="")
    
    def test_create_todo_item_with_whitespace_description_fails(self):
        """Test that creating a TodoItem with whitespace-only description raises an error."""
        with pytest.raises(InvalidTaskDescriptionError):
            TodoItem(id=1, description="   ")
    
    def test_mark_complete(self):
        """Test marking a task as complete."""
        item = TodoItem(id=1, description="Test task")
        original_updated_at = item.updated_at
        
        item.mark_complete()
        
        assert item.completed is True
        assert item.updated_at > original_updated_at
    
    def test_mark_incomplete(self):
        """Test marking a task as incomplete."""
        item = TodoItem(id=1, description="Test task", completed=True)
        original_updated_at = item.updated_at
        
        item.mark_incomplete()
        
        assert item.completed is False
        assert item.updated_at > original_updated_at
    
    def test_update_description(self):
        """Test updating a task's description."""
        item = TodoItem(id=1, description="Original task")
        original_updated_at = item.updated_at
        
        item.update_description("Updated task")
        
        assert item.description == "Updated task"
        assert item.updated_at > original_updated_at
    
    def test_update_description_with_empty_fails(self):
        """Test that updating a task's description with empty string raises an error."""
        item = TodoItem(id=1, description="Original task")
        
        with pytest.raises(InvalidTaskDescriptionError):
            item.update_description("")
    
    def test_update_description_with_whitespace_fails(self):
        """Test that updating a task's description with whitespace-only raises an error."""
        item = TodoItem(id=1, description="Original task")
        
        with pytest.raises(InvalidTaskDescriptionError):
            item.update_description("   ")
    
    def test_to_dict(self):
        """Test converting TodoItem to dictionary."""
        created_at = datetime(2023, 1, 1, 12, 0, 0)
        updated_at = datetime(2023, 1, 1, 12, 30, 0)
        
        item = TodoItem(
            id=1,
            description="Test task",
            completed=True,
            created_at=created_at,
            updated_at=updated_at
        )
        
        item_dict = item.to_dict()
        
        assert item_dict['id'] == 1
        assert item_dict['description'] == "Test task"
        assert item_dict['completed'] is True
        assert item_dict['created_at'] == "2023-01-01T12:00:00"
        assert item_dict['updated_at'] == "2023-01-01T12:30:00"
    
    def test_from_dict(self):
        """Test creating TodoItem from dictionary."""
        data = {
            'id': 1,
            'description': 'Test task',
            'completed': True,
            'created_at': '2023-01-01T12:00:00',
            'updated_at': '2023-01-01T12:30:00'
        }
        
        item = TodoItem.from_dict(data)
        
        assert item.id == 1
        assert item.description == "Test task"
        assert item.completed is True
        assert item.created_at == datetime(2023, 1, 1, 12, 0, 0)
        assert item.updated_at == datetime(2023, 1, 1, 12, 30, 0)
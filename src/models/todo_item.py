"""
TodoItem data model representing a single to-do task.
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional
import re
from src.utils.validation import validate_task_description


@dataclass
class TodoItem:
    """
    Represents a single to-do task.
    """
    id: int
    description: str
    completed: bool = False
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def __post_init__(self):
        """
        Validate the TodoItem after initialization.
        """
        if self.created_at is None:
            self.created_at = datetime.now()
        if self.updated_at is None:
            self.updated_at = datetime.now()

        # Validate description using utility function
        if not validate_task_description(self.description):
            raise ValueError("Task description cannot be empty or whitespace only")

        # Sanitize description to remove any problematic special characters if needed
        self.description = self.description.strip()
    
    def mark_complete(self):
        """
        Mark the task as complete and update the timestamp.
        """
        self.completed = True
        self.updated_at = datetime.now()
    
    def mark_incomplete(self):
        """
        Mark the task as incomplete and update the timestamp.
        """
        self.completed = False
        self.updated_at = datetime.now()
    
    def update_description(self, new_description: str):
        """
        Update the task description and update the timestamp.

        Args:
            new_description: New description for the task
        """
        if not validate_task_description(new_description):
            raise ValueError("Task description cannot be empty or whitespace only")

        self.description = new_description.strip()
        self.updated_at = datetime.now()
    
    def to_dict(self) -> dict:
        """
        Convert the TodoItem to a dictionary representation.
        
        Returns:
            Dictionary representation of the TodoItem
        """
        return {
            'id': self.id,
            'description': self.description,
            'completed': self.completed,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        """
        Create a TodoItem from a dictionary representation.
        
        Args:
            data: Dictionary representation of a TodoItem
            
        Returns:
            TodoItem instance
        """
        return cls(
            id=data['id'],
            description=data['description'],
            completed=data.get('completed', False),
            created_at=datetime.fromisoformat(data['created_at']) if data.get('created_at') else None,
            updated_at=datetime.fromisoformat(data['updated_at']) if data.get('updated_at') else None
        )
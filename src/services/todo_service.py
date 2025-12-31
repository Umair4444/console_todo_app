"""
TodoService handles the business logic for todo operations.
"""
from typing import List, Optional
from src.models.todo_item import TodoItem
from src.storage.file_storage import FileStorage
from src.utils.handlers import TaskNotFoundError, InvalidTaskDescriptionError
from src.config.settings import Settings
from src.utils.performance import measure_time
from src.utils.validation import validate_task_description
import json
from pathlib import Path


class TodoService:
    """
    Service class that handles business logic for todo operations.
    """
    
    def __init__(self, storage: FileStorage = None):
        """
        Initialize the TodoService.
        
        Args:
            storage: FileStorage instance for data persistence. 
                     If None, creates a default instance.
        """
        self.storage = storage or FileStorage(Settings.get_tasks_file_path())
    
    @measure_time
    def add_task(self, description: str) -> TodoItem:
        """
        Add a new task.

        Args:
            description: Description of the task

        Returns:
            Created TodoItem instance
        """
        # Validate description using utility
        if not validate_task_description(description):
            raise InvalidTaskDescriptionError()

        # Load existing tasks
        tasks_data = self.storage.load_tasks()

        # Determine new ID (auto-increment)
        new_id = 1
        if tasks_data:
            existing_ids = [task['id'] for task in tasks_data]
            new_id = max(existing_ids) + 1

        # Create new task
        new_task = TodoItem(
            id=new_id,
            description=description.strip()
        )

        # Add to tasks list and save
        tasks_data.append(new_task.to_dict())
        self.storage.save_tasks(tasks_data)

        return new_task
    
    @measure_time
    def get_all_tasks(self) -> List[TodoItem]:
        """
        Get all tasks.
        
        Returns:
            List of all TodoItem instances
        """
        tasks_data = self.storage.load_tasks()
        return [TodoItem.from_dict(task_data) for task_data in tasks_data]
    
    @measure_time
    def get_completed_tasks(self) -> List[TodoItem]:
        """
        Get all completed tasks.
        
        Returns:
            List of completed TodoItem instances
        """
        all_tasks = self.get_all_tasks()
        return [task for task in all_tasks if task.completed]
    
    @measure_time
    def get_incomplete_tasks(self) -> List[TodoItem]:
        """
        Get all incomplete tasks.
        
        Returns:
            List of incomplete TodoItem instances
        """
        all_tasks = self.get_all_tasks()
        return [task for task in all_tasks if not task.completed]
    
    @measure_time
    def update_task(self, task_id: int, new_description: str) -> TodoItem:
        """
        Update a task's description.

        Args:
            task_id: ID of the task to update
            new_description: New description for the task

        Returns:
            Updated TodoItem instance
        """
        # Validate description using utility
        if not validate_task_description(new_description):
            raise InvalidTaskDescriptionError()

        # Load existing tasks
        tasks_data = self.storage.load_tasks()

        # Find and update the task
        for i, task_data in enumerate(tasks_data):
            if task_data['id'] == task_id:
                # Update the task data
                task_data['description'] = new_description.strip()
                from datetime import datetime
                task_data['updated_at'] = datetime.now().isoformat()  # Update timestamp

                # Save updated tasks
                self.storage.save_tasks(tasks_data)

                # Return the updated task
                return TodoItem.from_dict(task_data)

        # If we get here, the task wasn't found
        raise TaskNotFoundError(task_id)
    
    @measure_time
    def mark_task_complete(self, task_id: int) -> TodoItem:
        """
        Mark a task as complete.
        
        Args:
            task_id: ID of the task to mark as complete
            
        Returns:
            Updated TodoItem instance
        """
        # Load existing tasks
        tasks_data = self.storage.load_tasks()
        
        # Find and update the task
        for i, task_data in enumerate(tasks_data):
            if task_data['id'] == task_id:
                # Update the task data
                task_data['completed'] = True
                from datetime import datetime
                task_data['updated_at'] = datetime.now().isoformat()  # Update timestamp

                # Save updated tasks
                self.storage.save_tasks(tasks_data)

                # Return the updated task
                return TodoItem.from_dict(task_data)
        
        # If we get here, the task wasn't found
        raise TaskNotFoundError(task_id)
    
    @measure_time
    def mark_task_incomplete(self, task_id: int) -> TodoItem:
        """
        Mark a task as incomplete.
        
        Args:
            task_id: ID of the task to mark as incomplete
            
        Returns:
            Updated TodoItem instance
        """
        # Load existing tasks
        tasks_data = self.storage.load_tasks()
        
        # Find and update the task
        for i, task_data in enumerate(tasks_data):
            if task_data['id'] == task_id:
                # Update the task data
                task_data['completed'] = False
                from datetime import datetime
                task_data['updated_at'] = datetime.now().isoformat()  # Update timestamp

                # Save updated tasks
                self.storage.save_tasks(tasks_data)

                # Return the updated task
                return TodoItem.from_dict(task_data)
        
        # If we get here, the task wasn't found
        raise TaskNotFoundError(task_id)
    
    @measure_time
    def delete_task(self, task_id: int) -> TodoItem:
        """
        Delete a task.
        
        Args:
            task_id: ID of the task to delete
            
        Returns:
            Deleted TodoItem instance
        """
        # Load existing tasks
        tasks_data = self.storage.load_tasks()
        
        # Find the task to delete
        for i, task_data in enumerate(tasks_data):
            if task_data['id'] == task_id:
                # Remove the task
                deleted_task_data = tasks_data.pop(i)
                
                # Save updated tasks
                self.storage.save_tasks(tasks_data)
                
                # Return the deleted task
                return TodoItem.from_dict(deleted_task_data)
        
        # If we get here, the task wasn't found
        raise TaskNotFoundError(task_id)
    
    @measure_time
    def export_tasks(self, filename: str) -> int:
        """
        Export tasks to a JSON file.
        
        Args:
            filename: Name of the file to export to
            
        Returns:
            Number of tasks exported
        """
        tasks_data = self.storage.load_tasks()
        
        # Write tasks to the specified file
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(tasks_data, f, indent=2, ensure_ascii=False)
        
        return len(tasks_data)
    
    @measure_time
    def import_tasks(self, filename: str) -> int:
        """
        Import tasks from a JSON file.
        
        Args:
            filename: Name of the file to import from
            
        Returns:
            Number of tasks imported
        """
        # Read tasks from the specified file
        with open(filename, 'r', encoding='utf-8') as f:
            imported_tasks_data = json.load(f)
        
        # Validate that imported data is a list
        if not isinstance(imported_tasks_data, list):
            raise ValueError("Imported file must contain a list of tasks")
        
        # Load existing tasks
        existing_tasks_data = self.storage.load_tasks()
        
        # Determine the highest existing ID to ensure unique IDs
        max_existing_id = 0
        if existing_tasks_data:
            max_existing_id = max(task['id'] for task in existing_tasks_data)
        
        # Adjust IDs of imported tasks to avoid conflicts
        for task_data in imported_tasks_data:
            if 'id' in task_data:
                task_data['id'] += max_existing_id
        
        # Combine existing and imported tasks
        all_tasks_data = existing_tasks_data + imported_tasks_data
        
        # Save combined tasks
        self.storage.save_tasks(all_tasks_data)
        
        return len(imported_tasks_data)
"""
Performance benchmarks for list operations.
"""
import pytest
import tempfile
import time
from pathlib import Path
from src.services.todo_service import TodoService
from src.storage.file_storage import FileStorage
from config.settings import Settings


class TestPerformanceBenchmarks:
    """Performance benchmarks for critical operations."""
    
    def test_list_operations_performance_under_threshold(self, temp_file):
        """Test that list operations complete within the performance threshold."""
        # Create a FileStorage with the temporary file
        storage = FileStorage(str(temp_file))
        
        # Create a TodoService with the storage
        service = TodoService(storage=storage)
        
        # Add a large number of tasks (up to 1000 as per requirements)
        num_tasks = min(1000, Settings.MAX_TASKS)  # Use the smaller of 1000 or MAX_TASKS
        
        for i in range(num_tasks):
            service.add_task(f"Task {i}: Sample task for performance testing")
        
        # Measure the time for get_all_tasks operation
        start_time = time.time()
        tasks = service.get_all_tasks()
        end_time = time.time()
        
        execution_time_ms = (end_time - start_time) * 1000
        
        # Verify we got all tasks
        assert len(tasks) == num_tasks
        
        # Check that execution time is under the threshold (100ms for 1000 tasks)
        threshold_ms = Settings.LIST_TASKS_THRESHOLD_MS
        assert execution_time_ms < threshold_ms, \
            f"get_all_tasks took {execution_time_ms:.2f}ms, which exceeds the threshold of {threshold_ms}ms"
        
        print(f"Performance test passed: get_all_tasks with {num_tasks} tasks took {execution_time_ms:.2f}ms")
    
    def test_add_task_performance(self, temp_file):
        """Test that adding tasks performs within acceptable limits."""
        storage = FileStorage(str(temp_file))
        service = TodoService(storage=storage)
        
        # Measure the time for adding a task
        start_time = time.time()
        task = service.add_task("Performance test task")
        end_time = time.time()
        
        execution_time_ms = (end_time - start_time) * 1000
        
        # Verify the task was added
        assert task is not None
        assert task.description == "Performance test task"
        
        # Check that execution time is reasonable (under 10ms for single task)
        assert execution_time_ms < 10, \
            f"Adding a single task took {execution_time_ms:.2f}ms, which is too slow"
        
        print(f"Performance test passed: Adding a task took {execution_time_ms:.2f}ms")
    
    def test_complete_task_performance(self, temp_file):
        """Test that marking tasks as complete performs within acceptable limits."""
        storage = FileStorage(str(temp_file))
        service = TodoService(storage=storage)
        
        # Add a task first
        task = service.add_task("Task for performance test")
        
        # Measure the time for marking a task as complete
        start_time = time.time()
        completed_task = service.mark_task_complete(task.id)
        end_time = time.time()
        
        execution_time_ms = (end_time - start_time) * 1000
        
        # Verify the task was marked as complete
        assert completed_task is not None
        assert completed_task.completed is True
        
        # Check that execution time is reasonable (under 10ms for single operation)
        assert execution_time_ms < 10, \
            f"Marking a task as complete took {execution_time_ms:.2f}ms, which is too slow"
        
        print(f"Performance test passed: Marking task complete took {execution_time_ms:.2f}ms")
"""
Performance monitoring utilities.
"""
import time
import functools
from typing import Callable, Any
from src.utils.handlers import get_logger

logger = get_logger(__name__)


def measure_time(func: Callable) -> Callable:
    """
    Decorator to measure the execution time of a function.
    
    Args:
        func: Function to measure
        
    Returns:
        Wrapped function with timing
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time_ms = (end_time - start_time) * 1000
        
        logger.info(f"{func.__name__} executed in {execution_time_ms:.2f} ms")
        return result
    
    return wrapper


class PerformanceTimer:
    """
    Context manager for measuring execution time of code blocks.
    """
    
    def __init__(self, name: str = "Operation"):
        """
        Initialize the performance timer.
        
        Args:
            name: Name of the operation being timed
        """
        self.name = name
        self.start_time = None
        self.end_time = None
    
    def __enter__(self):
        """
        Enter the context manager and start timing.
        
        Returns:
            PerformanceTimer instance
        """
        self.start_time = time.time()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Exit the context manager and log the execution time.
        """
        self.end_time = time.time()
        execution_time_ms = (self.end_time - self.start_time) * 1000
        logger.info(f"{self.name} completed in {execution_time_ms:.2f} ms")
    
    @property
    def elapsed_ms(self) -> float:
        """
        Get the elapsed time in milliseconds.
        
        Returns:
            Elapsed time in milliseconds
        """
        if self.start_time is None:
            return 0.0
        if self.end_time is None:
            return (time.time() - self.start_time) * 1000
        return (self.end_time - self.start_time) * 1000


def check_performance_threshold(operation_name: str, execution_time_ms: float, threshold_ms: float) -> bool:
    """
    Check if an operation's execution time is within the acceptable threshold.
    
    Args:
        operation_name: Name of the operation
        execution_time_ms: Execution time in milliseconds
        threshold_ms: Threshold in milliseconds
        
    Returns:
        True if within threshold, False otherwise
    """
    is_acceptable = execution_time_ms <= threshold_ms
    status = "✓" if is_acceptable else "✗"
    logger.info(f"{status} {operation_name}: {execution_time_ms:.2f}ms (threshold: {threshold_ms}ms)")
    return is_acceptable
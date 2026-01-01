"""
Basic test to verify the todo application works as expected.
"""
import subprocess
import sys
import tempfile
import os


def test_basic_functionality():
    """Test basic functionality of the todo application."""
    # Create a temporary file for testing
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as temp_file:
        temp_file_path = temp_file.name

    try:
        # Set environment variable to specify the tasks file
        env = os.environ.copy()
        env['TODO_TASKS_FILE'] = temp_file_path

        # Test adding a task
        result = subprocess.run([
            sys.executable, '-m', 'src.cli.cli_app',
            'add', 'Test', 'task'
        ], capture_output=True, text=True, env=env)

        print("Add task result:", result.returncode)
        print("Add task stdout:", result.stdout)
        print("Add task stderr:", result.stderr)

        # Test listing tasks
        result = subprocess.run([
            sys.executable, '-m', 'src.cli.cli_app',
            'list'
        ], capture_output=True, text=True, env=env)

        print("List tasks result:", result.returncode)
        print("List tasks stdout:", result.stdout)
        print("List tasks stderr:", result.stderr)

        # Verify that the task appears in the list
        assert "Test task" in result.stdout
        print("✓ Basic functionality test passed!")

    finally:
        # Clean up the temporary file
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)


if __name__ == "__main__":
    test_basic_functionality()
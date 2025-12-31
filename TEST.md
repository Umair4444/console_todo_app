# Testing Guide for Console Todo App

This document describes the testing strategy and how to run tests for the Console Todo App.

## Test Structure

The project follows a comprehensive testing approach with different types of tests:

### Unit Tests
Located in `tests/unit/`
- Test individual components in isolation
- Focus on models, utilities, and service methods
- Example: `tests/unit/test_models/test_todo_item.py`

### Contract Tests
Located in `tests/contract/`
- Test CLI commands and their expected behavior
- Verify input/output formats and error handling
- Example: `tests/contract/test_add_command.py`

### Integration Tests
Located in `tests/integration/`
- Test complete user journeys
- Verify multiple components work together
- Example: `tests/integration/test_cli_integration.py`

### Performance Tests
Located in `tests/performance/`
- Test performance benchmarks
- Ensure operations meet performance requirements
- Example: `tests/performance/test_performance_benchmarks.py`

## Running Tests

### Prerequisites
Make sure you have pytest installed:
```bash
pip install pytest
```

### Running All Tests
```bash
python -m pytest
```

### Running Specific Test Categories

#### Run all unit tests
```bash
python -m pytest tests/unit/
```

#### Run all contract tests
```bash
python -m pytest tests/contract/
```

#### Run all integration tests
```bash
python -m pytest tests/integration/
```

#### Run all performance tests
```bash
python -m pytest tests/performance/
```

### Running Specific Test Files
```bash
# Run a specific test file
python -m pytest tests/unit/test_models/test_todo_item.py

# Run with verbose output
python -m pytest tests/unit/test_models/test_todo_item.py -v
```

### Running Tests with Coverage
```bash
# Install coverage tool
pip install pytest-cov

# Run tests with coverage report
python -m pytest --cov=src
```

## Test Descriptions

### Unit Tests
- `tests/unit/test_models/test_todo_item.py`: Tests for the TodoItem model including creation, validation, and state transitions
- `tests/unit/test_storage/test_file_storage.py`: Tests for atomic write operations and file storage functionality

### Contract Tests
- `tests/contract/test_add_command.py`: Tests for the add command contract
- `tests/contract/test_list_command.py`: Tests for the list command contract
- `tests/contract/test_complete_command.py`: Tests for the complete command contract
- `tests/contract/test_incomplete_command.py`: Tests for the incomplete command contract
- `tests/contract/test_update_command.py`: Tests for the update command contract
- `tests/contract/test_delete_command.py`: Tests for the delete command contract
- `tests/contract/test_import_command.py`: Tests for the import command contract
- `tests/contract/test_export_command.py`: Tests for the export command contract

### Integration Tests
- `tests/integration/test_cli_integration.py`: Tests for complete user journeys combining multiple operations

### Performance Tests
- `tests/performance/test_performance_benchmarks.py`: Tests to ensure operations meet performance requirements (e.g., list operations under 100ms for 1000 tasks)

## Test Philosophy

The project follows a Test-Driven Development (TDD) approach where tests are written before implementation. Each user story has corresponding tests that verify the functionality works as expected.

Tests cover:
- Happy path scenarios
- Error conditions
- Edge cases
- Performance requirements
- Integration between components

## Adding New Tests

When adding new functionality:
1. Write tests first that define the expected behavior
2. Run the tests to confirm they fail (since the functionality doesn't exist yet)
3. Implement the functionality
4. Run the tests again to confirm they pass
5. Refactor if needed and ensure tests still pass
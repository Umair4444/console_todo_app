# Console To-Do Application Context for Qwen Code

## Project Overview
- **Name**: Console To-Do Application
- **Type**: Single console application with CLI visual enhancements
- **Language**: Python 3.8+
- **Status**: Active development

## Active Technologies
- Python 3.8+ (002-cli-visual-enhancement)
- rich library for CLI enhancements (002-cli-visual-enhancement)
- JSON for local storage (002-cli-visual-enhancement)

## Project Structure
src/
├── models/
│   ├── __init__.py
│   └── todo_item.py          # Defines the TodoItem data model
├── services/
│   ├── __init__.py
│   └── todo_service.py       # Handles business logic for todo operations
├── storage/
│   ├── __init__.py
│   └── file_storage.py       # Handles local file persistence
├── cli/
│   ├── __init__.py
│   └── cli_app.py            # CLI interface and command routing
└── __init__.py

tests/
├── unit/
│   ├── test_models/
│   ├── test_services/
│   └── test_storage/
├── integration/
│   └── test_cli_integration.py
└── conftest.py               # Test configuration

config/
├── __init__.py
└── settings.py               # Application configuration

docs/
└── quickstart.md             # User quickstart guide

## Key Commands
- Run tests: `pytest`
- Run application: `python run_todo.py`
- Check code style: `ruff check .`

## Recent Changes
- 002-cli-visual-enhancement: Added visual enhancements with emojis and arrow key navigation
- 002-cli-visual-enhancement: Added rich library for CLI enhancements
- 002-cli-visual-enhancement: Implemented terminal compatibility detection

## Language Conventions
- Python: Follow PEP 8 style guidelines with type hints
- Use meaningful variable names
- Modular architecture with clear separation of concerns
- Error handling with user-friendly messages

## Last updated: 2026-01-01
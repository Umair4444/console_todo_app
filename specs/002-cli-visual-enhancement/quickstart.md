# Quickstart: CLI Visual Enhancement

**Feature**: CLI Visual Enhancement
**Date**: 2026-01-01

## Overview
This guide explains how to use the enhanced CLI to-do application with visual elements and arrow key navigation.

## Installation
1. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
   
2. If not already installed, install the rich library for visual enhancements:
   ```bash
   pip install rich
   ```

## New Features

### Visual Enhancements
- Emojis and visual indicators are now displayed in the interface
- Different emojis represent different states of to-do items:
  - ✅ Completed tasks
  - 🔄 In-progress tasks
  - 📝 New tasks
  - 🗑️ Deleted tasks (in confirmation prompts)

### Arrow Key Navigation
- Navigate through lists using up/down arrow keys
- Press Enter to select the highlighted item
- Visual feedback shows which item is currently selected with a highlighted background and arrow indicator

### Keyboard Shortcuts
- `a` - Add a new to-do item
- `d` - Delete selected to-do item
- `e` - Edit selected to-do item
- `c` - Mark selected to-do as complete
- `q` - Quit the application
- Arrow keys (↑/↓) - Navigate through lists
- Enter - Confirm selection

## Usage Examples

### Viewing Your To-Do List
Run the application normally:
```bash
python run_todo.py list
```
You'll see your to-do items with emojis indicating their status and can navigate using arrow keys.

### Adding a New To-Do
```bash
python run_todo.py add "Buy groceries"
```
The new item will appear with a 📝 emoji indicating it's new.

### Completing a To-Do with Navigation
1. Run `python run_todo.py list` to see your list
2. Use the up/down arrow keys to navigate to the item you want to complete
3. Press `c` to mark it as complete (the emoji will change to ✅)

## Terminal Compatibility
The application automatically detects your terminal's capabilities:
- If emojis aren't supported, text alternatives will be used
- If colors aren't supported, the interface will fall back to basic text
- If keyboard input isn't supported, traditional number-based selection will be used

## Troubleshooting
- If emojis don't display correctly, ensure your terminal supports UTF-8 encoding
- If arrow keys don't work, check that your terminal supports keyboard input
- If colors don't appear, try a different terminal that supports ANSI colors
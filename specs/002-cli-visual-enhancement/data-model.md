# Data Model: CLI Visual Enhancement

**Feature**: CLI Visual Enhancement
**Date**: 2026-01-01

## Entities

### Visual Elements
- **Name**: Visual Elements
- **Description**: Visual indicators (emojis, colors, symbols) that enhance the user interface
- **Fields**:
  - emoji: string (e.g., ✅, 🔄, 📝, 🗑️)
  - color: string (e.g., "green", "red", "yellow")
  - symbol: string (e.g., ">", "*", "-")
  - description: string (text alternative for accessibility)

### Navigation State
- **Name**: Navigation State
- **Description**: Current selection position in interactive menus and lists
- **Fields**:
  - current_index: integer (0-based index of currently selected item)
  - total_items: integer (total number of items in the list)
  - menu_id: string (identifier for the current menu/list)
  - last_action: string (last navigation action: up, down, enter, etc.)

### Terminal Compatibility
- **Name**: Terminal Compatibility
- **Description**: Information about the user's terminal capabilities for displaying visual elements
- **Fields**:
  - supports_color: boolean (whether terminal supports color)
  - supports_emoji: boolean (whether terminal supports emojis)
  - supports_keyboard: boolean (whether terminal supports keyboard input)
  - color_depth: string (e.g., "standard", "256", "truecolor")
  - encoding: string (character encoding, e.g., "UTF-8")

## Relationships
- Each TodoItem can have associated Visual Elements for display
- Navigation State is associated with a specific menu/list context
- Terminal Compatibility affects how Visual Elements are rendered

## State Transitions
- Navigation State changes when user presses arrow keys (up/down) or performs selection (enter)
- Visual Elements may change based on Terminal Compatibility detection

## Validation Rules
- current_index in Navigation State must be between 0 and total_items-1
- emoji field in Visual Elements must be a valid Unicode emoji or fallback character
- Terminal Compatibility fields must accurately reflect actual terminal capabilities
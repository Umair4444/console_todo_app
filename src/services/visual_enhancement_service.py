"""
Visual Enhancement Service handles the business logic for visual enhancements like emojis,
colors, and terminal compatibility detection.
"""
from typing import Dict, List, Optional
from dataclasses import dataclass
import sys
import os


@dataclass
class VisualElement:
    """
    Represents a visual element with its display properties.
    """
    emoji: str
    color: str
    symbol: str
    description: str


@dataclass
class NavigationState:
    """
    Represents the state of navigation in the CLI application.
    """
    current_index: int
    total_items: int
    menu_id: str
    last_action: str


@dataclass
class TerminalCompatibility:
    """
    Represents the terminal's compatibility with various visual features.
    """
    supports_color: bool
    supports_emoji: bool
    supports_keyboard: bool
    color_depth: int  # 32, 256, or 16m
    encoding: str


class VisualEnhancementService:
    """
    Service class that handles visual enhancements for the CLI application.
    """

    def __init__(self):
        """
        Initialize the Visual Enhancement Service.
        """
        self.emoji_mapping = {
            'completed': '✅',
            'in_progress': '🔄',
            'active': '📝',
            'deleted': '❌',
            'add': '➕',
            'list': '📋',
            'update': '✏️',
            'delete': '🗑️',
            'exit': '🚪',
            'help': '❓',
            'success': '✅',
            'error': '❌',
            'warning': '⚠️',
            'info': 'ℹ️',
        }
        
        self.color_mapping = {
            'completed': 'green',
            'in_progress': 'yellow',
            'active': 'blue',
            'deleted': 'red',
            'add': 'cyan',
            'list': 'magenta',
            'update': 'yellow',
            'delete': 'red',
            'exit': 'bright_black',
            'help': 'bright_cyan',
            'success': 'green',
            'error': 'red',
            'warning': 'yellow',
            'info': 'blue',
        }

    def get_visual_element(self, element_type: str) -> VisualElement:
        """
        Get a visual element for the specified type.

        Args:
            element_type: Type of visual element to retrieve

        Returns:
            VisualElement instance
        """
        emoji = self.emoji_mapping.get(element_type, '❓')
        color = self.color_mapping.get(element_type, 'white')
        symbol = self._get_fallback_symbol(element_type)
        description = self._get_element_description(element_type)
        
        return VisualElement(
            emoji=emoji,
            color=color,
            symbol=symbol,
            description=description
        )

    def _get_fallback_symbol(self, element_type: str) -> str:
        """
        Get a fallback symbol for when emojis aren't supported.

        Args:
            element_type: Type of visual element

        Returns:
            Fallback symbol string
        """
        fallbacks = {
            'completed': '[X]',
            'in_progress': '[~]',
            'active': '[O]',
            'deleted': '[D]',
            'add': '[+]',
            'list': '[L]',
            'update': '[U]',
            'delete': '[DEL]',
            'exit': '[EXIT]',
            'help': '[?]',
            'success': '[OK]',
            'error': '[ERR]',
            'warning': '[!]',
            'info': '[INFO]',
        }
        return fallbacks.get(element_type, '[?]')

    def _get_element_description(self, element_type: str) -> str:
        """
        Get a description for the visual element.

        Args:
            element_type: Type of visual element

        Returns:
            Description string
        """
        descriptions = {
            'completed': 'Task completed',
            'in_progress': 'Task in progress',
            'active': 'Active task',
            'deleted': 'Deleted task',
            'add': 'Add new task',
            'list': 'List tasks',
            'update': 'Update task',
            'delete': 'Delete task',
            'exit': 'Exit application',
            'help': 'Help information',
            'success': 'Success message',
            'error': 'Error message',
            'warning': 'Warning message',
            'info': 'Information message',
        }
        return descriptions.get(element_type, 'Unknown element')

    def get_todo_status_emoji(self, completed: bool, in_progress: bool = False) -> str:
        """
        Get the appropriate emoji for a todo item based on its status.

        Args:
            completed: Whether the task is completed
            in_progress: Whether the task is in progress

        Returns:
            Emoji string for the task status
        """
        if completed:
            return self.emoji_mapping['completed']
        elif in_progress:
            return self.emoji_mapping['in_progress']
        else:
            return self.emoji_mapping['active']

    def get_todo_status_color(self, completed: bool, in_progress: bool = False) -> str:
        """
        Get the appropriate color for a todo item based on its status.

        Args:
            completed: Whether the task is completed
            in_progress: Whether the task is in progress

        Returns:
            Color string for the task status
        """
        if completed:
            return self.color_mapping['completed']
        elif in_progress:
            return self.color_mapping['in_progress']
        else:
            return self.color_mapping['active']

    def get_fallback_for_emoji(self, emoji: str) -> str:
        """
        Get a fallback representation for an emoji.

        Args:
            emoji: The emoji to get a fallback for

        Returns:
            Fallback string representation
        """
        # Find the key that corresponds to this emoji
        for key, value in self.emoji_mapping.items():
            if value == emoji:
                return self._get_fallback_symbol(key)
        
        # If we can't find a mapping, return a generic fallback
        return '[?]'

    def format_task_with_visuals(self, task_id: int, description: str, completed: bool, in_progress: bool = False) -> str:
        """
        Format a task with appropriate visual elements.

        Args:
            task_id: ID of the task
            description: Description of the task
            completed: Whether the task is completed
            in_progress: Whether the task is in progress

        Returns:
            Formatted string with visual elements
        """
        emoji = self.get_todo_status_emoji(completed, in_progress)
        color = self.get_todo_status_color(completed, in_progress)
        
        # Format the task with the visual elements
        status_indicator = f"[{color}]{emoji}[/]" if self._supports_color() else self._get_fallback_symbol(
            'completed' if completed else ('in_progress' if in_progress else 'active')
        )
        
        return f"{status_indicator} {task_id}. {description}"

    def _supports_color(self) -> bool:
        """
        Check if the terminal supports color.

        Returns:
            True if color is supported, False otherwise
        """
        # Check if we're running in a terminal that supports color
        if not sys.stdout.isatty():
            return False

        # Check environment variables
        if os.environ.get('TERM') in ('dumb', 'unknown'):
            return False

        # On Windows, check for color support
        if sys.platform.startswith('win'):
            # Windows 10 version 10.0.10586 and later support ANSI colors
            if sys.version_info >= (3, 7):
                # Python 3.7+ has better color support on Windows
                return True
            else:
                # For older versions, check if we're in a modern terminal
                return os.environ.get('WT_SESSION') is not None  # Windows Terminal

        # On Unix-like systems, check TERM
        return os.environ.get('TERM') != 'dumb'

    def detect_terminal_compatibility(self) -> TerminalCompatibility:
        """
        Detect the terminal's compatibility with various visual features.

        Returns:
            TerminalCompatibility instance with detected capabilities
        """
        supports_color = self._supports_color()
        supports_emoji = self._supports_emoji()
        supports_keyboard = True  # We assume keyboard support for now
        color_depth = self._detect_color_depth()
        encoding = sys.stdout.encoding or 'utf-8'

        return TerminalCompatibility(
            supports_color=supports_color,
            supports_emoji=supports_emoji,
            supports_keyboard=supports_keyboard,
            color_depth=color_depth,
            encoding=encoding
        )

    def _supports_emoji(self) -> bool:
        """
        Check if the terminal supports emojis.

        Returns:
            True if emoji is supported, False otherwise
        """
        # Try to print a simple emoji to test support
        try:
            # Test with a simple emoji
            test_emoji = '✅'
            # Encode and decode to check if it's supported
            test_emoji.encode(sys.stdout.encoding or 'utf-8')
            return True
        except UnicodeEncodeError:
            return False

    def _detect_color_depth(self) -> int:
        """
        Detect the color depth of the terminal.

        Returns:
            Color depth (32 for basic, 256 for 256-color, 16m for true color)
        """
        # Check environment variables
        if os.environ.get('COLORTERM') == 'truecolor' or os.environ.get('TERM_PROGRAM') == 'iTerm.app':
            return 16777216  # 16m (true color)
        
        # Check TERM environment variable
        term = os.environ.get('TERM', '')
        if '256color' in term:
            return 256
        
        # Default to basic color support
        return 32
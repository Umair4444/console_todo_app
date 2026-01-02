"""
Visual Elements model representing visual components for the CLI application.
"""
from dataclasses import dataclass
from typing import Optional


@dataclass
class VisualElement:
    """
    Represents a visual element with its properties.
    """
    emoji: str
    color: str
    symbol: str
    description: str

    def __post_init__(self):
        """
        Validate the VisualElement after initialization.
        """
        if not self.emoji:
            raise ValueError("Emoji cannot be empty")
        if not self.color:
            raise ValueError("Color cannot be empty")
        if not self.symbol:
            raise ValueError("Symbol cannot be empty")
        if not self.description:
            raise ValueError("Description cannot be empty")


@dataclass
class NavigationState:
    """
    Represents the state of navigation in the CLI application.
    """
    current_index: int
    total_items: int
    menu_id: str
    last_action: str

    def __post_init__(self):
        """
        Validate the NavigationState after initialization.
        """
        if self.total_items < 0:
            raise ValueError("Total items cannot be negative")
        if self.total_items == 0:
            # For empty lists, current_index should be -1
            if self.current_index != -1:
                raise ValueError("Current index must be -1 for empty lists")
        else:
            # For non-empty lists, current_index must be valid
            if self.current_index < 0:
                raise ValueError("Current index cannot be negative for non-empty lists")
            if self.current_index >= self.total_items:
                raise ValueError("Current index cannot be greater than or equal to total items")
        if not self.menu_id:
            raise ValueError("Menu ID cannot be empty")


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

    def __post_init__(self):
        """
        Validate the TerminalCompatibility after initialization.
        """
        if self.color_depth not in [32, 256, 16777216]:  # Basic, 256-color, true color
            raise ValueError("Color depth must be 32, 256, or 16777216 (true color)")
        if not self.encoding:
            raise ValueError("Encoding cannot be empty")


@dataclass
class MenuOption:
    """
    Represents a menu option with its properties.
    """
    id: str
    display_text: str
    action: str

    def __post_init__(self):
        """
        Validate the MenuOption after initialization.
        """
        if not self.id:
            raise ValueError("Menu option ID cannot be empty")
        if not self.display_text:
            raise ValueError("Display text cannot be empty")
        if not self.action:
            raise ValueError("Action cannot be empty")


@dataclass
class ApplicationState:
    """
    Represents the application state with its properties.
    """
    current_menu: str
    waiting_for_confirmation: bool
    last_key_press: Optional[str] = None

    def __post_init__(self):
        """
        Validate the ApplicationState after initialization.
        """
        if not self.current_menu:
            raise ValueError("Current menu cannot be empty")
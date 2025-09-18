"""
Utility modules for cross-platform GUI and platform detection.

This package provides utilities for:
- Platform detection and configuration
- Modern GUI styling and theming
- Cross-platform font and color management
- GUI initialization and testing
"""

# Import all public APIs
from .platform import (
    get_platform_info, is_windows, is_macos, is_linux,
    configure_macos_app, get_cursor_name,
    CURRENT_PLATFORM, IS_WINDOWS, IS_MACOS, IS_LINUX
)
from .styling import (
    get_system_font, get_title_font, get_text_font, get_theme_colors,
    apply_modern_style, create_modern_button, configure_modern_window,
    configure_window_for_platform
)
from .gui import (
    ensure_gui_initialized, create_root_window, test_gui_availability
)

__all__ = [
    # Platform utilities
    "get_platform_info", "is_windows", "is_macos", "is_linux",
    "configure_macos_app", "get_cursor_name",
    "CURRENT_PLATFORM", "IS_WINDOWS", "IS_MACOS", "IS_LINUX",
    # Styling utilities
    "get_system_font", "get_title_font", "get_text_font", "get_theme_colors",
    "apply_modern_style", "create_modern_button", "configure_modern_window",
    "configure_window_for_platform",
    # GUI utilities
    "ensure_gui_initialized", "create_root_window", "test_gui_availability"
]
"""
Platform detection and cross-platform utility functions.

This module provides utilities for detecting the current platform and
configuring GUI elements appropriately for Windows, macOS, and Linux.
"""

import platform
import subprocess
import os
from typing import Dict, Tuple, Any


# Platform detection constants
CURRENT_PLATFORM = platform.system().lower()
IS_WINDOWS = CURRENT_PLATFORM == 'windows'
IS_MACOS = CURRENT_PLATFORM == 'darwin'
IS_LINUX = CURRENT_PLATFORM == 'linux'


def get_platform_info() -> Dict[str, Any]:
    """
    Get comprehensive platform information.
    
    Returns:
        Dictionary containing platform details including system, release,
        version, machine, and processor information.
    """
    return {
        "system": platform.system(),
        "release": platform.release(),
        "version": platform.version(),
        "machine": platform.machine(),
        "processor": platform.processor(),
        "platform": CURRENT_PLATFORM,
        "is_windows": IS_WINDOWS,
        "is_macos": IS_MACOS,
        "is_linux": IS_LINUX
    }


def is_windows() -> bool:
    """Check if running on Windows."""
    return IS_WINDOWS


def is_macos() -> bool:
    """Check if running on macOS."""
    return IS_MACOS


def is_linux() -> bool:
    """Check if running on Linux."""
    return IS_LINUX


def configure_macos_app():
    """
    Configure macOS-specific application settings.
    
    Attempts to bring the Python process to the foreground on macOS
    using AppleScript. Fails silently if osascript is not available.
    """
    if IS_MACOS:
        try:
            # Try to bring Python to front on macOS
            subprocess.run([
                'osascript', '-e', 
                f'tell application "System Events" to set frontmost of first process whose unix id is {os.getpid()} to true'
            ], check=False, capture_output=True)
        except Exception:
            pass  # Ignore if osascript is not available


def get_cursor_name() -> str:
    """
    Get the appropriate cursor name for clickable elements.
    
    Returns:
        String name of cursor appropriate for the platform.
    """
    if IS_WINDOWS:
        return "hand2"
    else:
        return "hand1"
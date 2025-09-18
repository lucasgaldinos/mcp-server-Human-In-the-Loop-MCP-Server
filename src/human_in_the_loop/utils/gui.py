"""
GUI initialization utilities for cross-platform operation.

This module provides utilities for initializing and testing GUI availability
across different platforms (Windows, macOS, Linux).
"""

import threading
import tkinter as tk
from typing import Optional

# Global variable to ensure GUI is initialized properly
_gui_initialized = False
_gui_lock = threading.Lock()


def ensure_gui_initialized() -> bool:
    """
    Ensure GUI is properly initialized for the current platform.
    
    Returns:
        bool: True if GUI initialization was successful, False otherwise
    """
    global _gui_initialized
    
    with _gui_lock:
        if _gui_initialized:
            return True
            
        try:
            # Test if we can create a tkinter root window
            test_root = tk.Tk()
            test_root.withdraw()  # Hide the test window
            test_root.destroy()
            _gui_initialized = True
            return True
        except Exception as e:
            print(f"GUI initialization failed: {e}")
            return False


def create_root_window(title: str = "Human-in-the-Loop Dialog") -> Optional[tk.Tk]:
    """
    Create and configure a root tkinter window.
    
    Args:
        title: Window title
        
    Returns:
        Configured tkinter root window or None if creation fails
    """
    try:
        if not ensure_gui_initialized():
            return None
            
        root = tk.Tk()
        root.title(title)
        root.withdraw()  # Start hidden
        
        # Platform-specific window configuration
        from .platform import IS_MACOS, IS_WINDOWS
        
        if IS_MACOS:
            # macOS window styling
            root.configure(bg="#FFFFFF")
            try:
                # Try to bring window to front on macOS
                root.call('::tk::unsupported::MacWindowStyle', 'style', root._w, 'document')
                root.lift()
                root.attributes('-topmost', True)
                root.after_idle(lambda: root.attributes('-topmost', False))
            except:
                pass
        elif IS_WINDOWS:
            # Windows window styling
            root.configure(bg="#FFFFFF")
            try:
                root.attributes('-topmost', True)
                root.after_idle(lambda: root.attributes('-topmost', False))
            except:
                pass
        
        return root
    except Exception as e:
        print(f"Failed to create root window: {e}")
        return None


def test_gui_availability() -> dict:
    """
    Test GUI system availability and return status information.
    
    Returns:
        Dictionary with GUI status information
    """
    from .platform import CURRENT_PLATFORM, IS_WINDOWS, IS_MACOS, IS_LINUX
    
    try:
        gui_available = ensure_gui_initialized()
        
        return {
            "gui_available": gui_available,
            "platform": CURRENT_PLATFORM,
            "is_windows": IS_WINDOWS,
            "is_macos": IS_MACOS,
            "is_linux": IS_LINUX,
            "status": "healthy" if gui_available else "gui_unavailable"
        }
    except Exception as e:
        return {
            "gui_available": False,
            "platform": CURRENT_PLATFORM,
            "error": str(e),
            "status": "unhealthy"
        }
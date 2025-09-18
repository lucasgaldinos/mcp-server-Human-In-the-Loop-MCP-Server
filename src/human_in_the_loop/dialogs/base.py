"""
Base dialog class and common GUI initialization utilities.

This module provides the foundation for all dialog types with common
functionality for window management, threading, and GUI initialization.
"""

import tkinter as tk
import threading
from typing import Optional, Any
from ..utils.styling import configure_modern_window, configure_window_for_platform
from ..utils.platform import IS_MACOS, IS_WINDOWS


# Global variables for GUI initialization
_gui_initialized = False
_gui_lock = threading.Lock()


def ensure_gui_initialized() -> bool:
    """
    Ensure GUI subsystem is properly initialized.
    
    Returns:
        True if GUI is available, False otherwise
    """
    global _gui_initialized
    with _gui_lock:
        if not _gui_initialized:
            try:
                test_root = tk.Tk()
                test_root.withdraw()
                
                # Platform-specific initialization
                if IS_MACOS:
                    # macOS-specific configuration
                    test_root.call('wm', 'attributes', '.', '-topmost', '1')
                    from ..utils.platform import configure_macos_app
                    configure_macos_app()
                elif IS_WINDOWS:
                    # Windows-specific configuration
                    test_root.attributes('-topmost', True)
                
                test_root.destroy()
                _gui_initialized = True
            except Exception as e:
                print(f"Warning: GUI initialization failed: {e}")
                _gui_initialized = False
        return _gui_initialized


class BaseDialog:
    """
    Base class for all dialog types.
    
    Provides common functionality for:
    - Window creation and styling
    - Result handling
    - Platform-specific configuration
    - Error handling
    """
    
    def __init__(self, parent, title: str):
        """
        Initialize base dialog.
        
        Args:
            parent: Parent tkinter widget
            title: Dialog window title
        """
        self.result: Optional[Any] = None
        self.title = title
        self.parent = parent
        
        # Create the dialog window
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(title)
        
        # Set grab, but handle potential errors gracefully
        try:
            self.dialog.grab_set()
        except tk.TclError:
            pass  # Ignore grab errors in case another dialog has grab
            
        self.dialog.resizable(False, False)
        
        # Apply modern window styling
        configure_modern_window(self.dialog)
        
        # Handle window close
        self.dialog.protocol("WM_DELETE_WINDOW", self.on_cancel)
        
    def center_window(self):
        """
        Center the dialog window on screen.
        
        Should be called after all widgets are created and window
        size is determined.
        """
        self.dialog.update_idletasks()
        width = self.dialog.winfo_width()
        height = self.dialog.winfo_height()
        screen_width = self.dialog.winfo_screenwidth()
        screen_height = self.dialog.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        
        # Platform-specific adjustments
        if IS_MACOS:
            y = max(50, y - 50)
        elif IS_WINDOWS:
            y = max(30, y - 30)
            
        self.dialog.geometry(f"{width}x{height}+{x}+{y}")
    
    def on_cancel(self):
        """Handle dialog cancellation."""
        self.result = None
        self.dialog.destroy()
    
    def on_ok(self):
        """Handle dialog confirmation. Should be overridden by subclasses."""
        self.dialog.destroy()
    
    def show(self) -> Optional[Any]:
        """
        Show the dialog and return the result.
        
        Returns:
            Dialog result or None if cancelled
        """
        # Center the window after all widgets are created
        self.center_window()
        
        # Wait for dialog completion
        self.dialog.wait_window()
        
        return self.result


def create_dialog_safely(dialog_class, *args, **kwargs) -> Optional[Any]:
    """
    Create a dialog safely with proper error handling.
    
    Args:
        dialog_class: Dialog class to instantiate
        *args: Arguments to pass to dialog constructor
        **kwargs: Keyword arguments to pass to dialog constructor
        
    Returns:
        Dialog result or None if error occurred
    """
    try:
        # Ensure GUI is initialized
        if not ensure_gui_initialized():
            return None
            
        # Create temporary root if needed
        root = tk.Tk()
        root.withdraw()
        
        # Create and show dialog
        dialog = dialog_class(root, *args, **kwargs)
        result = dialog.show()
        
        # Clean up
        root.destroy()
        
        return result
        
    except Exception as e:
        print(f"Error creating dialog: {e}")
        return None
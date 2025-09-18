"""
Information dialog for displaying messages to the user.

This module provides a simple dialog for showing information
messages that require user acknowledgment.
"""

import tkinter as tk
from typing import Optional
from .base import BaseDialog
from ..utils.styling import (
    get_theme_colors, get_title_font, get_system_font, create_modern_button
)
from ..utils.platform import IS_WINDOWS


class InfoDialog(BaseDialog):
    """
    Modern information dialog for displaying messages.
    
    Shows a message with an OK button for acknowledgment.
    """
    
    def __init__(self, parent, title: str, message: str):
        """
        Initialize information dialog.
        
        Args:
            parent: Parent tkinter widget
            title: Dialog window title
            message: Message to display to user
        """
        self.message = message
        self.theme_colors = get_theme_colors()
        
        super().__init__(parent, title)
        
        # Set size based on platform and content
        if IS_WINDOWS:
            self.dialog.geometry("440x200")
        else:
            self.dialog.geometry("420x180")
        
        self._create_widgets()
        self._setup_bindings()
    
    def _create_widgets(self):
        """Create and layout dialog widgets."""
        # Create the main frame
        main_frame = tk.Frame(self.dialog, bg=self.theme_colors["bg_primary"])
        main_frame.pack(fill="both", expand=True, padx=24, pady=20)
        
        # Title label
        title_label = tk.Label(
            main_frame,
            text=self.title,
            bg=self.theme_colors["bg_primary"],
            fg=self.theme_colors["fg_primary"],
            font=get_title_font(),
            anchor="w"
        )
        title_label.pack(fill="x", pady=(0, 12))
        
        # Message label
        message_label = tk.Label(
            main_frame,
            text=self.message,
            bg=self.theme_colors["bg_primary"],
            fg=self.theme_colors["fg_secondary"],
            font=get_system_font(),
            wraplength=370,
            justify="left",
            anchor="w"
        )
        message_label.pack(fill="x", pady=(0, 24))
        
        # Button frame
        button_frame = tk.Frame(main_frame, bg=self.theme_colors["bg_primary"])
        button_frame.pack(fill="x")
        
        # Create OK button
        self.ok_button = create_modern_button(
            button_frame, "OK", self.on_ok, "primary", self.theme_colors
        )
        self.ok_button.pack(side=tk.RIGHT)
    
    def _setup_bindings(self):
        """Set up keyboard shortcuts and event bindings."""
        self.dialog.bind('<Return>', lambda e: self.on_ok())
        self.dialog.bind('<Escape>', lambda e: self.on_ok())
    
    def on_ok(self):
        """Handle OK button click."""
        self.result = True
        self.dialog.destroy()
    
    def on_cancel(self):
        """Handle dialog cancellation (treat as acknowledged)."""
        self.result = True
        self.dialog.destroy()


def show_info(title: str, message: str) -> bool:
    """
    Show an information dialog.
    
    Args:
        title: Dialog window title
        message: Message to display
        
    Returns:
        True when user acknowledges the message
    """
    try:
        root = tk.Tk()
        root.withdraw()
        dialog = InfoDialog(root, title, message)
        result = dialog.show()
        root.destroy()
        return result if result is not None else True
    except Exception as e:
        print(f"Error in info dialog: {e}")
        return True
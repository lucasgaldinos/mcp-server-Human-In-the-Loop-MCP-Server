"""
Confirmation dialog for yes/no decisions.

This module provides a modern confirmation dialog that presents
a message to the user and asks for a yes/no decision.
"""

import tkinter as tk
from typing import Optional
from .base import BaseDialog
from ..utils.styling import (
    get_theme_colors, get_title_font, get_system_font, create_modern_button
)
from ..utils.platform import IS_WINDOWS


class ConfirmationDialog(BaseDialog):
    """
    Modern confirmation dialog for yes/no decisions.
    
    Displays a message and provides Yes/No buttons for user response.
    """
    
    def __init__(self, parent, title: str, message: str):
        """
        Initialize confirmation dialog.
        
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
            self.dialog.geometry("440x220")
        else:
            self.dialog.geometry("420x200")
        
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
        
        # Create modern buttons
        self.yes_button = create_modern_button(
            button_frame, "Yes", self.on_yes, "primary", self.theme_colors
        )
        self.yes_button.pack(side=tk.RIGHT, padx=(8, 0))
        
        self.no_button = create_modern_button(
            button_frame, "No", self.on_no, "secondary", self.theme_colors
        )
        self.no_button.pack(side=tk.RIGHT)
    
    def _setup_bindings(self):
        """Set up keyboard shortcuts and event bindings."""
        self.dialog.bind('<Return>', lambda e: self.on_yes())
        self.dialog.bind('<Escape>', lambda e: self.on_no())
    
    def on_yes(self):
        """Handle Yes button click."""
        self.result = True
        self.dialog.destroy()
    
    def on_no(self):
        """Handle No button click."""
        self.result = False
        self.dialog.destroy()
    
    def on_cancel(self):
        """Handle dialog cancellation (treat as No)."""
        self.result = False
        self.dialog.destroy()


def show_confirmation(title: str, message: str) -> bool:
    """
    Show a confirmation dialog.
    
    Args:
        title: Dialog window title
        message: Message to display
        
    Returns:
        True if user clicked Yes, False otherwise
    """
    try:
        root = tk.Tk()
        root.withdraw()
        dialog = ConfirmationDialog(root, title, message)
        result = dialog.show()
        root.destroy()
        return result if result is not None else False
    except Exception as e:
        print(f"Error in confirmation dialog: {e}")
        return False
"""
Input dialog for getting text, number, or other user input.

This module provides a modern, cross-platform input dialog that can
handle different input types including text, integers, and floats.
"""

import tkinter as tk
from typing import Optional, Union, Literal
from .base import BaseDialog
from ..utils.styling import (
    get_theme_colors, get_title_font, get_system_font, create_modern_button
)
from ..utils.platform import IS_WINDOWS, IS_MACOS


class InputDialog(BaseDialog):
    """
    Modern input dialog for getting user input.
    
    Supports different input types:
    - text: String input (default)
    - integer: Integer number input
    - float: Floating point number input
    """
    
    def __init__(self, parent, title: str, prompt: str, 
                 default_value: str = "", 
                 input_type: Literal["text", "integer", "float"] = "text"):
        """
        Initialize input dialog.
        
        Args:
            parent: Parent tkinter widget
            title: Dialog window title
            prompt: Prompt text to display to user
            default_value: Default value to pre-fill in input field
            input_type: Type of input validation to apply
        """
        self.input_type = input_type
        self.theme_colors = get_theme_colors()
        
        super().__init__(parent, title)
        
        # Set size based on platform
        if IS_WINDOWS:
            self.dialog.geometry("420x280")
        else:
            self.dialog.geometry("400x260")
        
        self._create_widgets(prompt, default_value)
        self._setup_bindings()
        
        # Focus on entry
        self.entry.focus_set()
    
    def _create_widgets(self, prompt: str, default_value: str):
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
        title_label.pack(fill="x", pady=(0, 8))
        
        # Prompt label
        prompt_label = tk.Label(
            main_frame,
            text=prompt,
            bg=self.theme_colors["bg_primary"],
            fg=self.theme_colors["fg_secondary"],
            font=get_system_font(),
            wraplength=350,
            justify="left",
            anchor="w"
        )
        prompt_label.pack(fill="x", pady=(0, 20))
        
        # Input field
        input_frame = tk.Frame(main_frame, bg=self.theme_colors["bg_primary"])
        input_frame.pack(fill="x", pady=(0, 24))
        
        self.entry = tk.Entry(
            input_frame,
            font=get_system_font(),
            bg=self.theme_colors["bg_primary"],
            fg=self.theme_colors["fg_primary"],
            relief="solid",
            borderwidth=1,
            highlightthickness=1,
            highlightcolor=self.theme_colors["accent_color"],
            highlightbackground=self.theme_colors["border_color"],
            insertbackground=self.theme_colors["accent_color"]
        )
        self.entry.pack(fill="x", ipady=8, ipadx=12)
        
        if default_value:
            self.entry.insert(0, default_value)
            self.entry.select_range(0, tk.END)
        
        # Button frame
        button_frame = tk.Frame(main_frame, bg=self.theme_colors["bg_primary"])
        button_frame.pack(fill="x")
        
        # Create modern buttons
        self.ok_button = create_modern_button(
            button_frame, "OK", self.on_ok, "primary", self.theme_colors
        )
        self.ok_button.pack(side=tk.RIGHT, padx=(8, 0))
        
        self.cancel_button = create_modern_button(
            button_frame, "Cancel", self.on_cancel, "secondary", self.theme_colors
        )
        self.cancel_button.pack(side=tk.RIGHT)
    
    def _setup_bindings(self):
        """Set up keyboard shortcuts and event bindings."""
        self.dialog.bind('<Return>', lambda e: self.on_ok())
        self.dialog.bind('<Escape>', lambda e: self.on_cancel())
    
    def on_ok(self):
        """Handle OK button click with input validation."""
        value = self.entry.get()
        
        if self.input_type == "integer":
            try:
                self.result = int(value) if value else None
            except ValueError:
                self.result = None
        elif self.input_type == "float":
            try:
                self.result = float(value) if value else None
            except ValueError:
                self.result = None
        else:
            self.result = value if value else None
            
        self.dialog.destroy()


def create_input_dialog(title: str, prompt: str, default_value: str = "", 
                       input_type: Literal["text", "integer", "float"] = "text") -> Optional[Union[str, int, float]]:
    """
    Create and show an input dialog.
    
    Args:
        title: Dialog window title
        prompt: Prompt text to display
        default_value: Default value to pre-fill
        input_type: Type of input validation
        
    Returns:
        User input value, or None if cancelled
    """
    try:
        root = tk.Tk()
        root.withdraw()
        dialog = InputDialog(root, title, prompt, default_value, input_type)
        result = dialog.show()
        root.destroy()
        return result
    except Exception as e:
        print(f"Error in input dialog: {e}")
        return None
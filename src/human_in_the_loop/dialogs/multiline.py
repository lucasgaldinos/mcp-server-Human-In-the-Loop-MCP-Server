"""
Multiline input dialog for getting longer text input.

This module provides a dialog with a text area for entering
multiple lines of text, suitable for detailed descriptions,
code, or other long-form content.
"""

import tkinter as tk
from typing import Optional
from .base import BaseDialog
from ..utils.styling import (
    get_theme_colors, get_title_font, get_system_font, 
    create_modern_button, apply_modern_style
)
from ..utils.platform import IS_WINDOWS, IS_MACOS


class MultilineInputDialog(BaseDialog):
    """
    Modern multiline input dialog for entering longer text.
    
    Provides a resizable text area with scrollbar for entering
    multi-line text content.
    """
    
    def __init__(self, parent, title: str, prompt: str, default_value: str = ""):
        """
        Initialize multiline input dialog.
        
        Args:
            parent: Parent tkinter widget
            title: Dialog window title
            prompt: Prompt text to display
            default_value: Default text to pre-fill in text area
        """
        self.prompt = prompt
        self.default_value = default_value
        self.theme_colors = get_theme_colors()
        
        super().__init__(parent, title)
        
        # Set size based on platform
        if IS_MACOS:
            self.dialog.geometry("580x480")
        elif IS_WINDOWS:
            self.dialog.geometry("600x500")
        else:
            self.dialog.geometry("550x450")
        
        # Allow resizing for this dialog
        self.dialog.resizable(True, True)
        
        self._create_widgets()
        self._setup_bindings()
        
        # Focus on text widget
        self.text_widget.focus_set()
        
        # Platform-specific focus handling
        if IS_MACOS:
            self.dialog.after(100, lambda: self.text_widget.focus_set())
    
    def _create_widgets(self):
        """Create and layout dialog widgets."""
        # Create the main frame with modern styling
        main_frame = tk.Frame(self.dialog, bg=self.theme_colors["bg_primary"])
        main_frame.pack(fill="both", expand=True, padx=24, pady=20)
        
        # Configure grid weights
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        # Add modern title label
        title_label = tk.Label(
            main_frame,
            text=self.title,
            bg=self.theme_colors["bg_primary"],
            fg=self.theme_colors["fg_primary"],
            font=get_title_font(),
            anchor="w"
        )
        title_label.grid(row=0, column=0, sticky="ew", pady=(0, 8))
        
        # Add prompt label with modern styling
        prompt_label = tk.Label(
            main_frame,
            text=self.prompt,
            bg=self.theme_colors["bg_primary"],
            fg=self.theme_colors["fg_secondary"],
            font=get_system_font(),
            wraplength=520,
            justify="left",
            anchor="w"
        )
        prompt_label.grid(row=1, column=0, sticky="ew", pady=(0, 20))
        
        # Create text widget container with modern styling
        text_container = tk.Frame(main_frame, bg=self.theme_colors["bg_primary"])
        text_container.grid(row=2, column=0, sticky="nsew", pady=(0, 24))
        text_container.columnconfigure(0, weight=1)
        text_container.rowconfigure(0, weight=1)
        
        # Modern text widget
        self.text_widget = tk.Text(text_container, height=12)
        apply_modern_style(self.text_widget, "text", self.theme_colors)
        self.text_widget.grid(row=0, column=0, sticky="nsew", padx=(0, 2))
        
        # Modern scrollbar for text widget
        text_scrollbar = tk.Scrollbar(text_container, orient="vertical", command=self.text_widget.yview)
        apply_modern_style(text_scrollbar, "scrollbar", self.theme_colors)
        text_scrollbar.grid(row=0, column=1, sticky="ns")
        self.text_widget.configure(yscrollcommand=text_scrollbar.set)
        
        # Set default value
        if self.default_value:
            self.text_widget.insert("1.0", self.default_value)
        
        # Modern button frame
        button_frame = tk.Frame(main_frame, bg=self.theme_colors["bg_primary"])
        button_frame.grid(row=3, column=0, sticky="ew")
        
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
        # Use Ctrl+Enter for OK in multiline dialog
        self.dialog.bind('<Control-Return>', lambda e: self.on_ok())
        self.dialog.bind('<Escape>', lambda e: self.on_cancel())
    
    def on_ok(self):
        """Handle OK button click."""
        self.result = self.text_widget.get("1.0", tk.END).strip()
        self.dialog.destroy()


def create_multiline_dialog(title: str, prompt: str, default_value: str = "") -> Optional[str]:
    """
    Create and show a multiline input dialog.
    
    Args:
        title: Dialog window title
        prompt: Prompt text to display
        default_value: Default text to pre-fill
        
    Returns:
        User input text, or None if cancelled
    """
    try:
        root = tk.Tk()
        root.withdraw()
        dialog = MultilineInputDialog(root, title, prompt, default_value)
        result = dialog.show()
        root.destroy()
        return result
    except Exception as e:
        print(f"Error in multiline dialog: {e}")
        return None
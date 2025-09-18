"""
Choice dialog for selecting from multiple options.

This module provides a dialog that presents a list of choices
for the user to select from, supporting both single and multiple selection.
"""

import tkinter as tk
from typing import List, Union, Optional
from .base import BaseDialog
from ..utils.styling import (
    get_theme_colors, get_title_font, get_system_font, 
    create_modern_button, apply_modern_style
)
from ..utils.platform import IS_WINDOWS, IS_MACOS


class ChoiceDialog(BaseDialog):
    """
    Modern choice dialog for selecting from multiple options.
    
    Supports both single and multiple selection modes.
    """
    
    def __init__(self, parent, title: str, prompt: str, 
                 choices: List[str], allow_multiple: bool = False):
        """
        Initialize choice dialog.
        
        Args:
            parent: Parent tkinter widget
            title: Dialog window title
            prompt: Prompt text to display
            choices: List of choice strings
            allow_multiple: Whether to allow multiple selections
        """
        self.prompt = prompt
        self.choices = choices
        self.allow_multiple = allow_multiple
        self.theme_colors = get_theme_colors()
        
        super().__init__(parent, title)
        
        # Set size based on platform
        if IS_MACOS:
            self.dialog.geometry("480x400")
        elif IS_WINDOWS:
            self.dialog.geometry("500x420")
        else:
            self.dialog.geometry("450x350")
        
        # Allow resizing for this dialog
        self.dialog.resizable(True, True)
        
        self._create_widgets()
        self._setup_bindings()
        
        # Focus on listbox and select first item
        self.listbox.focus_set()
        if choices:
            self.listbox.selection_set(0)
            
        # Platform-specific focus handling
        if IS_MACOS:
            self.dialog.after(100, lambda: self.listbox.focus_set())
    
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
            wraplength=450,
            justify="left",
            anchor="w"
        )
        prompt_label.grid(row=1, column=0, sticky="ew", pady=(0, 20))
        
        # Create choice selection widget with modern container
        list_container = tk.Frame(main_frame, bg=self.theme_colors["bg_primary"])
        list_container.grid(row=2, column=0, sticky="nsew", pady=(0, 24))
        list_container.columnconfigure(0, weight=1)
        list_container.rowconfigure(0, weight=1)
        
        # Modern listbox with styling
        if self.allow_multiple:
            self.listbox = tk.Listbox(list_container, selectmode=tk.MULTIPLE, height=8)
        else:
            self.listbox = tk.Listbox(list_container, selectmode=tk.SINGLE, height=8)
        
        apply_modern_style(self.listbox, "listbox", self.theme_colors)
        
        for choice in self.choices:
            self.listbox.insert(tk.END, choice)
        self.listbox.grid(row=0, column=0, sticky="nsew", padx=(0, 2))
        
        # Modern scrollbar
        scrollbar = tk.Scrollbar(list_container, orient="vertical", command=self.listbox.yview)
        apply_modern_style(scrollbar, "scrollbar", self.theme_colors)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.listbox.configure(yscrollcommand=scrollbar.set)
        
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
        self.dialog.bind('<Return>', lambda e: self.on_ok())
        self.dialog.bind('<Escape>', lambda e: self.on_cancel())
    
    def on_ok(self):
        """Handle OK button click."""
        selection = self.listbox.curselection()
        if selection:
            selected_items = [self.listbox.get(i) for i in selection]
            # Return single item if single selection, list if multiple
            self.result = selected_items if self.allow_multiple or len(selected_items) > 1 else selected_items[0]
        else:
            self.result = None
        self.dialog.destroy()


def show_choice_dialog(title: str, prompt: str, choices: List[str], 
                      allow_multiple: bool = False) -> Optional[Union[str, List[str]]]:
    """
    Show a choice dialog.
    
    Args:
        title: Dialog window title
        prompt: Prompt text to display
        choices: List of choice strings
        allow_multiple: Whether to allow multiple selections
        
    Returns:
        Selected choice(s) or None if cancelled
    """
    try:
        root = tk.Tk()
        root.withdraw()
        dialog = ChoiceDialog(root, title, prompt, choices, allow_multiple)
        result = dialog.show()
        root.destroy()
        return result
    except Exception as e:
        print(f"Error in choice dialog: {e}")
        return None
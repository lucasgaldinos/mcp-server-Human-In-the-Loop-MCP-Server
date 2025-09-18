"""
Dialog modules for user interaction.

This package provides modern, cross-platform GUI dialogs for:
- Text input (single and multi-line)
- Choice selection (single and multiple)
- Confirmation (yes/no)
- Information display

All dialogs follow modern design principles and adapt to platform conventions.
"""

# Import all dialog classes and functions
from .base import BaseDialog, ensure_gui_initialized, create_dialog_safely
from .input import InputDialog, create_input_dialog
from .choice import ChoiceDialog, show_choice_dialog
from .multiline import MultilineInputDialog, create_multiline_dialog
from .confirmation import ConfirmationDialog, show_confirmation
from .info import InfoDialog, show_info

__all__ = [
    # Base functionality
    "BaseDialog", "ensure_gui_initialized", "create_dialog_safely",
    # Input dialogs
    "InputDialog", "create_input_dialog",
    # Choice dialogs
    "ChoiceDialog", "show_choice_dialog", 
    # Multiline input
    "MultilineInputDialog", "create_multiline_dialog",
    # Confirmation dialogs
    "ConfirmationDialog", "show_confirmation",
    # Info dialogs
    "InfoDialog", "show_info"
]
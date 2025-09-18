#!/usr/bin/env python3
"""
Test the dialog functions with new modular structure.
"""
import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.human_in_the_loop.utils.platform import get_platform_info
from src.human_in_the_loop.utils.gui import test_gui_availability


def test_platform_detection():
    """Test that platform detection works correctly."""
    platform_info = get_platform_info()
    assert "system" in platform_info
    assert "release" in platform_info
    print(f"Platform: {platform_info['system']} {platform_info['release']}")


def test_gui_availability_check():
    """Test GUI availability detection."""
    gui_status = test_gui_availability()
    assert "gui_available" in gui_status
    assert "platform" in gui_status
    print(f"GUI Available: {gui_status['gui_available']}")
    return gui_status["gui_available"]


def test_module_imports():
    """Test that all modules can be imported correctly."""
    from src.human_in_the_loop.utils import (
        get_platform_info, get_system_font, get_theme_colors,
        ensure_gui_initialized
    )
    from src.human_in_the_loop.tools import register_tools, register_prompts
    print("All module imports successful")


def test_dialog_imports():
    """Test that dialog classes can be imported."""
    from src.human_in_the_loop.dialogs import (
        InputDialog, MultilineInputDialog, ChoiceDialog, 
        ConfirmationDialog, InfoDialog
    )
    print("Dialog imports successful")
    
    # Test that classes exist and have expected attributes
    assert hasattr(InputDialog, '__init__')
    assert hasattr(ChoiceDialog, '__init__')
    assert hasattr(MultilineInputDialog, '__init__')
    assert hasattr(ConfirmationDialog, '__init__')
    assert hasattr(InfoDialog, '__init__')
    print("Dialog classes have expected methods")


def test_server_import():
    """Test that the main server can be imported."""
    import human_loop_server
    assert hasattr(human_loop_server, 'main')
    assert hasattr(human_loop_server, 'mcp')
    print("Server import successful")


if __name__ == "__main__":
    print("Testing modular structure...")
    
    # Run tests
    test_platform_detection()
    gui_available = test_gui_availability_check()
    test_module_imports()
    test_dialog_imports()
    test_server_import()
    
    print(f"All tests completed! GUI available: {gui_available}")
    print("✓ Project modularization successful!")

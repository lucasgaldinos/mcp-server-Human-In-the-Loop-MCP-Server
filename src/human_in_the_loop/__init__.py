"""
Human-in-the-Loop MCP Server

A Model Context Protocol (MCP) server that provides interactive GUI dialogs
for getting human input, choices, and confirmations during AI workflows.

This package enables LLMs to pause execution and request human feedback,
input, or decisions through modern cross-platform GUI dialogs.

Modules:
    dialogs: Dialog classes for different types of user interaction
    tools: MCP tool implementations
    utils: Utility functions for platform detection and GUI styling
"""

__version__ = "1.0.0"
__author__ = "Human-in-the-Loop MCP Server Contributors"

# Import main components for easy access
from .dialogs.base import BaseDialog
from .utils.platform import get_platform_info, is_windows, is_macos, is_linux

__all__ = [
    "BaseDialog",
    "get_platform_info",
    "is_windows", 
    "is_macos",
    "is_linux",
]
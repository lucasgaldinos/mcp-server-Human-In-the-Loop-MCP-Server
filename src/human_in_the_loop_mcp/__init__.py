"""
Human-in-the-Loop MCP Server Package

A clean, production-ready Model Context Protocol server providing 5 essential 
human interaction tools through VS Code's native Command Palette interface.

This package focuses on simplicity and reliability, providing only tools that 
actually work within MCP's constraints.
"""

__version__ = "4.1.0"
__author__ = "Human-in-the-Loop MCP Server Team"
__license__ = "MIT"

from .server import main

__all__ = ["main"]
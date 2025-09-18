"""
MCP tools for human-in-the-loop interactions.

This module provides all the tool registration functions needed
to set up a FastMCP server with human-in-the-loop capabilities.
"""

from .dialog_tools import register_tools
from .prompts import register_prompts

__all__ = ["register_tools", "register_prompts"]
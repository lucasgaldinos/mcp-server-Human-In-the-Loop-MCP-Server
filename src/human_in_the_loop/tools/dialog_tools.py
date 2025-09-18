"""
MCP (Model Context Protocol) tools for human-in-the-loop interactions.

This module defines the FastMCP tool functions that expose the dialog
functionality to LLMs and AI agents through the MCP protocol.
"""

import sys
import platform
from typing import Dict, Any, List, Literal
from pydantic import Field
from typing import Annotated
from fastmcp import FastMCP, Context

from ..dialogs import (
    create_input_dialog, show_choice_dialog, create_multiline_dialog,
    show_confirmation, show_info, ensure_gui_initialized
)
from ..utils.platform import CURRENT_PLATFORM, IS_WINDOWS, IS_MACOS, IS_LINUX


def register_tools(mcp: FastMCP):
    """Register all human-in-the-loop tools with the MCP server."""
    
    @mcp.tool()
    async def get_user_input(
        title: Annotated[str, Field(description="Title of the input dialog window")],
        prompt: Annotated[str, Field(description="The prompt/question to show to the user")],
        default_value: Annotated[str, Field(description="Default value to pre-fill in the input field")] = "",
        input_type: Annotated[Literal["text", "integer", "float"], Field(description="Type of input expected")] = "text",
        ctx: Context = None
    ) -> Dict[str, Any]:
        """
        Create an input dialog window for the user to enter text, numbers, or other data.
        
        This tool opens a GUI dialog box where the user can input information that the LLM needs.
        Perfect for getting specific details, clarifications, or data from the user.
        """
        try:
            if ctx:
                await ctx.info(f"Requesting user input: {prompt}")
            
            # Ensure GUI is initialized
            if not ensure_gui_initialized():
                return {
                    "success": False,
                    "error": "GUI system not available",
                    "cancelled": False,
                    "platform": CURRENT_PLATFORM
                }
            
            # Create the dialog directly (tkinter must run on main thread)
            result = create_input_dialog(title, prompt, default_value, input_type)
            
            if result is not None:
                if ctx:
                    await ctx.info(f"User provided input: {result}")
                return {
                    "success": True,
                    "user_input": result,
                    "input_type": input_type,
                    "cancelled": False,
                    "platform": CURRENT_PLATFORM
                }
            else:
                if ctx:
                    await ctx.warning("User cancelled the input dialog")
                return {
                    "success": False,
                    "user_input": None,
                    "input_type": input_type,
                    "cancelled": True,
                    "platform": CURRENT_PLATFORM
                }
        
        except Exception as e:
            if ctx:
                await ctx.error(f"Error creating input dialog: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "cancelled": False,
                "platform": CURRENT_PLATFORM
            }

    @mcp.tool()
    async def get_user_choice(
        title: Annotated[str, Field(description="Title of the choice dialog window")],
        prompt: Annotated[str, Field(description="The prompt/question to show to the user")],
        choices: Annotated[List[str], Field(description="List of choices to present to the user")],
        allow_multiple: Annotated[bool, Field(description="Whether user can select multiple choices")] = False,
        ctx: Context = None
    ) -> Dict[str, Any]:
        """
        Create a choice dialog window for the user to select from multiple options.
        
        This tool opens a GUI dialog box with a list of choices where the user can select
        one or multiple options. Perfect for getting decisions, preferences, or selections from the user.
        """
        try:
            if ctx:
                await ctx.info(f"Requesting user choice: {prompt}")
                await ctx.debug(f"Available choices: {choices}")
            
            # Ensure GUI is initialized
            if not ensure_gui_initialized():
                return {
                    "success": False,
                    "error": "GUI system not available",
                    "cancelled": False,
                    "platform": CURRENT_PLATFORM
                }
            
            # Create the dialog directly (tkinter must run on main thread)
            result = show_choice_dialog(title, prompt, choices, allow_multiple)
            
            if result is not None:
                if ctx:
                    await ctx.info(f"User selected: {result}")
                return {
                    "success": True,
                    "selected_choice": result,
                    "selected_choices": result if isinstance(result, list) else [result],
                    "allow_multiple": allow_multiple,
                    "cancelled": False,
                    "platform": CURRENT_PLATFORM
                }
            else:
                if ctx:
                    await ctx.warning("User cancelled the choice dialog")
                return {
                    "success": False,
                    "selected_choice": None,
                    "selected_choices": [],
                    "allow_multiple": allow_multiple,
                    "cancelled": True,
                    "platform": CURRENT_PLATFORM
                }
        
        except Exception as e:
            if ctx:
                await ctx.error(f"Error creating choice dialog: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "cancelled": False,
                "platform": CURRENT_PLATFORM
            }

    @mcp.tool()
    async def get_multiline_input(
        title: Annotated[str, Field(description="Title of the input dialog window")],
        prompt: Annotated[str, Field(description="The prompt/question to show to the user")],
        default_value: Annotated[str, Field(description="Default text to pre-fill in the text area")] = "",
        ctx: Context = None
    ) -> Dict[str, Any]:
        """
        Create a multi-line text input dialog for the user to enter longer text content.
        
        This tool opens a GUI dialog box with a large text area where the user can input
        multiple lines of text. Perfect for getting detailed descriptions, code, or long-form content.
        """
        try:
            if ctx:
                await ctx.info(f"Requesting multiline user input: {prompt}")
            
            # Ensure GUI is initialized
            if not ensure_gui_initialized():
                return {
                    "success": False,
                    "error": "GUI system not available",
                    "cancelled": False,
                    "platform": CURRENT_PLATFORM
                }
            
            # Create the dialog directly (tkinter must run on main thread)
            result = create_multiline_dialog(title, prompt, default_value)
            
            if result is not None:
                if ctx:
                    await ctx.info(f"User provided multiline input ({len(result)} characters)")
                return {
                    "success": True,
                    "user_input": result,
                    "character_count": len(result),
                    "line_count": len(result.split('\n')),
                    "cancelled": False,
                    "platform": CURRENT_PLATFORM
                }
            else:
                if ctx:
                    await ctx.warning("User cancelled the multiline input dialog")
                return {
                    "success": False,
                    "user_input": None,
                    "cancelled": True,
                    "platform": CURRENT_PLATFORM
                }
        
        except Exception as e:
            if ctx:
                await ctx.error(f"Error creating multiline input dialog: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "cancelled": False,
                "platform": CURRENT_PLATFORM
            }

    @mcp.tool()
    async def show_confirmation_dialog(
        title: Annotated[str, Field(description="Title of the confirmation dialog")],
        message: Annotated[str, Field(description="The message to show to the user")],
        ctx: Context = None
    ) -> Dict[str, Any]:
        """
        Show a confirmation dialog with Yes/No buttons.
        
        This tool displays a message to the user and asks for confirmation.
        Perfect for getting approval before proceeding with an action.
        """
        try:
            if ctx:
                await ctx.info(f"Requesting user confirmation: {message}")
            
            # Ensure GUI is initialized
            if not ensure_gui_initialized():
                return {
                    "success": False,
                    "error": "GUI system not available",
                    "confirmed": False,
                    "platform": CURRENT_PLATFORM
                }
            
            # Create the dialog directly (tkinter must run on main thread)
            result = show_confirmation(title, message)
            
            if ctx:
                await ctx.info(f"User confirmation result: {'Yes' if result else 'No'}")
            
            return {
                "success": True,
                "confirmed": result,
                "response": "yes" if result else "no",
                "platform": CURRENT_PLATFORM
            }
        
        except Exception as e:
            if ctx:
                await ctx.error(f"Error showing confirmation dialog: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "confirmed": False,
                "platform": CURRENT_PLATFORM
            }

    @mcp.tool()
    async def show_info_message(
        title: Annotated[str, Field(description="Title of the information dialog")],
        message: Annotated[str, Field(description="The information message to show to the user")],
        ctx: Context = None
    ) -> Dict[str, Any]:
        """
        Show an information message to the user.
        
        This tool displays an informational message dialog to notify the user about something.
        The user just needs to click OK to acknowledge the message.
        """
        try:
            if ctx:
                await ctx.info(f"Showing info message to user: {message}")
            
            # Ensure GUI is initialized
            if not ensure_gui_initialized():
                return {
                    "success": False,
                    "error": "GUI system not available",
                    "platform": CURRENT_PLATFORM
                }
            
            # Create the dialog directly (tkinter must run on main thread)
            result = show_info(title, message)
            
            if ctx:
                await ctx.info("Info message acknowledged by user")
            
            return {
                "success": True,
                "acknowledged": result,
                "platform": CURRENT_PLATFORM
            }
        
        except Exception as e:
            if ctx:
                await ctx.error(f"Error showing info message: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "platform": CURRENT_PLATFORM
            }

    @mcp.tool()
    async def health_check() -> Dict[str, Any]:
        """Check if the Human-in-the-Loop server is running and GUI is available."""
        try:
            gui_available = ensure_gui_initialized()
            
            return {
                "status": "healthy" if gui_available else "degraded",
                "gui_available": gui_available,
                "server_name": "Human-in-the-Loop Server",
                "platform": CURRENT_PLATFORM,
                "platform_details": {
                    "system": platform.system(),
                    "release": platform.release(),
                    "version": platform.version(),
                    "machine": platform.machine(),
                    "processor": platform.processor()
                },
                "python_version": sys.version.split()[0],
                "is_windows": IS_WINDOWS,
                "is_macos": IS_MACOS,
                "is_linux": IS_LINUX,
                "tools_available": [
                    "get_user_input",
                    "get_user_choice", 
                    "get_multiline_input",
                    "show_confirmation_dialog",
                    "show_info_message",
                    "get_human_loop_prompt"
                ]
            }
        except Exception as e:
            return {
                "status": "unhealthy",
                "gui_available": False,
                "error": str(e),
                "platform": CURRENT_PLATFORM
            }
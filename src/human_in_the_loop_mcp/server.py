#!/usr/bin/env python3
"""
Human-in-the-Loop MCP Server v4.1 - Clean Implementation

A Model Context Protocol (MCP) server that provides clean, working human interaction tools
for AI assistants through VS Code's native Command Palette interface.

This version focuses on the 5 core tools that actually work, removing all the failed
multiline solutions that created read-only resources or inaccessible files.

Author: Human-in-the-Loop MCP Server Team
Version: 4.1.0
License: MIT
"""

import logging
import sys
from typing import Dict, Any, Optional

# FastMCP 2.12 imports
from fastmcp import FastMCP, Context
from pydantic import Field

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("human-loop-server")

# Initialize MCP server
mcp = FastMCP("Human-in-the-Loop MCP Server v4.1")

@mcp.tool()
async def get_user_input(
    ctx: Context,
    prompt: str = Field(description="The question/prompt to show the user"),
    title: Optional[str] = Field(default=None, description="Optional title for the input dialog"),
    default_value: Optional[str] = Field(default=None, description="Optional default value to pre-fill"),
    input_type: str = Field(default="text", description="Type of input expected (text, integer, float)")
) -> Dict[str, Any]:
    """
    Get single-line input from user using native VS Code dialog.
    
    Creates a Command Palette-style input prompt directly in VS Code.
    Best for simple, single-line inputs.
    
    Args:
        prompt: The question/prompt to show the user
        title: Optional title for the input dialog  
        default_value: Optional default value to pre-fill
        input_type: Type of input expected (text, integer, float)
    
    Returns:
        The user's input as a string, or error message if cancelled
    """
    try:
        await ctx.info(f"Requesting user input: {prompt}")
        
        # Use ctx.elicit for native VS Code Command Palette input
        result = await ctx.elicit(
            message=prompt,
            response_type=str
        )
        
        if result.action != "accept":
            return {
                "success": False,
                "error": "User cancelled input request",
                "result": f"User cancelled input request: {prompt}"
            }
        
        input_value = result.data
        
        # Type conversion if requested
        if input_type == "integer":
            try:
                input_value = str(int(input_value))
            except ValueError:
                return {
                    "success": False,
                    "error": f"Invalid integer: {input_value}",
                    "result": f"Invalid integer value: {input_value}"
                }
        elif input_type == "float":
            try:
                input_value = str(float(input_value))
            except ValueError:
                return {
                    "success": False,
                    "error": f"Invalid float: {input_value}",
                    "result": f"Invalid float value: {input_value}"
                }
        
        await ctx.info(f"User input received: {input_value}")
        return {
            "success": True,
            "result": input_value
        }
        
    except Exception as e:
        await ctx.error(f"Error in get_user_input: {e}")
        return {
            "success": False,
            "error": str(e),
            "result": f"Error getting user input: {e}"
        }

@mcp.tool()
async def get_user_choice(
    ctx: Context,
    prompt: str = Field(description="The question/prompt to show the user"),
    choices: list[str] = Field(description="List of available choices"),
    title: Optional[str] = Field(default=None, description="Optional title for the choice dialog"),
    allow_multiple: bool = Field(default=False, description="Whether user can select multiple choices (Note: MCP elicitations only support single choice)")
) -> Dict[str, Any]:
    """
    Let user choose from multiple options using native VS Code dialog.
    
    Creates a Command Palette-style choice picker directly in VS Code.
    User will see native selection interface, not JSON responses.
    
    Args:
        prompt: The question/prompt to show the user
        choices: List of available choices
        title: Optional title for the choice dialog
        allow_multiple: Whether user can select multiple choices (Note: MCP elicitations only support single choice)
    
    Returns:
        The user's choice as a string, or error message if cancelled
    """
    try:
        await ctx.info(f"Requesting user choice: {prompt}")
        
        if not choices:
            return {
                "success": False,
                "error": "No choices provided",
                "result": "Error: No choices provided for selection"
            }
        
        # Use ctx.elicit with choice list for native VS Code choice picker
        result = await ctx.elicit(
            message=prompt,
            response_type=choices
        )
        
        if result.action != "accept":
            return {
                "success": False,
                "error": "User cancelled choice request",
                "result": f"User cancelled choice request: {prompt}"
            }
        
        await ctx.info(f"User choice received: {result.data}")
        return {
            "success": True,
            "result": f"User selected: {result.data}"
        }
        
    except Exception as e:
        await ctx.error(f"Error in get_user_choice: {e}")
        return {
            "success": False,
            "error": str(e),
            "result": f"Error getting user choice: {e}"
        }

@mcp.tool()
async def show_confirmation_dialog(
    ctx: Context,
    message: str = Field(description="The confirmation message to show"),
    title: Optional[str] = Field(default=None, description="Optional title for the confirmation dialog"),
    confirm_text: str = Field(default="Yes", description="Text for the confirm button"),
    cancel_text: str = Field(default="No", description="Text for the cancel button")
) -> Dict[str, Any]:
    """
    Ask user for confirmation using native VS Code dialog.
    
    Creates a Command Palette-style confirmation prompt directly in VS Code.
    User will see native Yes/No interface, not JSON responses.
    
    Args:
        message: The confirmation message to show
        title: Optional title for the confirmation dialog
        confirm_text: Text for the confirm button (default: "Yes")
        cancel_text: Text for the cancel button (default: "No")
    
    Returns:
        Confirmation result as a string, or error message if cancelled
    """
    try:
        await ctx.info(f"Requesting user confirmation: {message}")
        
        # Use ctx.elicit with None response type for confirmation
        result = await ctx.elicit(
            message=f"{message}\n\nChoose {confirm_text} or {cancel_text}:",
            response_type=None
        )
        
        if result.action == "accept":
            await ctx.info(f"User confirmed: {message}")
            return {
                "success": True,
                "result": f"User confirmed: {message}"
            }
        else:
            await ctx.info(f"User declined: {message}")
            return {
                "success": True,
                "result": f"User declined: {message}"
            }
        
    except Exception as e:
        await ctx.error(f"Error in show_confirmation_dialog: {e}")
        return {
            "success": False,
            "error": str(e),
            "result": f"Error showing confirmation: {e}"
        }

@mcp.tool()
async def show_info_message(
    ctx: Context,
    message: str = Field(description="The information message to display"),
    title: Optional[str] = Field(default=None, description="Optional title for the info dialog"),
    info_type: str = Field(default="info", description="Type of information (info, warning, error, success)")
) -> Dict[str, Any]:
    """
    Display information to user using native VS Code dialog.
    
    Creates a Command Palette-style info display directly in VS Code.
    User will see native information dialog, not JSON responses.
    
    Args:
        message: The information message to display
        title: Optional title for the info dialog
        info_type: Type of information (info, warning, error, success)
    
    Returns:
        Confirmation that message was displayed
    """
    try:
        await ctx.info(f"Displaying {info_type} message: {message}")
        
        # Use ctx.elicit for info display with user acknowledgment
        result = await ctx.elicit(
            message=f"[{info_type.upper()}] {message}\n\nPress any key to continue...",
            response_type=str
        )
        
        await ctx.info(f"User acknowledged {info_type} message")
        return {
            "success": True,
            "result": f"Message displayed and acknowledged: {message}"
        }
        
    except Exception as e:
        await ctx.error(f"Error in show_info_message: {e}")

@mcp.tool()
async def health_check(ctx: Context) -> Dict[str, Any]:
    """
    Check the health and status of the Human-in-the-Loop MCP Server v4.1.
    
    Returns comprehensive information about server capabilities,
    interaction patterns, and operational status.
    
    Returns:
        Health check results and server information
    """
    try:
        await ctx.info("Performing health check")
        
        health_data = {
            "status": "HEALTHY",
            "version": "4.1.0",
            "server_name": "Human-in-the-Loop MCP Server",
            "capabilities": {
                "single_line_input": "✅ Native VS Code Command Palette input",
                "multiple_choice": "✅ Native choice picker with enum support",
                "confirmations": "✅ Native boolean confirmation dialogs",
                "info_display": "✅ Formatted message display with acknowledgment",
                "error_handling": "✅ Comprehensive error handling and logging"
            },
            "interaction_patterns": {
                "elicitations": "✅ Native VS Code Command Palette interface",
                "input_validation": "✅ Type conversion and validation",
                "user_cancellation": "✅ Graceful handling of cancelled operations",
                "logging": "✅ Comprehensive operation logging"
            },
            "mcp_compliance": {
                "fastmcp_version": "2.12",
                "context_usage": "✅ Proper Context dependency injection",
                "elicitation_patterns": "✅ Current ctx.elicit() API usage",
                "tool_decorators": "✅ @mcp.tool() decorators",
                "type_safety": "✅ Pydantic Field definitions"
            },
            "limitations": {
                "multiline_input": "❌ MCP elicitations are single-line only",
                "file_editing": "❌ No file editing capabilities",
                "rich_ui": "❌ Limited to Command Palette interface",
                "external_resources": "❌ No external resource creation"
            },
            "tools_available": [
                "get_user_input - Single-line text/number input",
                "get_user_choice - Multiple choice selection",
                "show_confirmation_dialog - Yes/no confirmations",
                "show_info_message - Information display",
                "health_check - Server status check"
            ],
            "total_tools": 5,
            "timestamp": ctx.request_id,
            "environment": "VS Code MCP Integration"
        }
        
        await ctx.info("Health check completed successfully")
        return {
            "success": True,
            "result": health_data
        }
        
    except Exception as e:
        await ctx.error(f"Error in health_check: {e}")
        return {
            "success": False,
            "error": str(e),
            "result": f"Health check failed: {e}"
        }

def main():
    """Main entry point for the Human-in-the-Loop MCP Server v4.1"""
    try:
        logger.info("Starting Human-in-the-Loop MCP Server v4.1")
        logger.info("Available tools: get_user_input, get_user_choice, show_confirmation_dialog, show_info_message, health_check")
        
        # Run the MCP server
        mcp.run()
        
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
    except Exception as e:
        logger.error(f"Server error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
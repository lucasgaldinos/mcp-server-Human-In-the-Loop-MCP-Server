#!/usr/bin/env python3
"""
Human-in-the-Loop MCP Server v3.0 - Native VS Code Elicitations

This version uses FastMCP's elicit() function to create native VS Code input dialogs
instead of returning complex JSON responses. When tools are called, users will see
actual Command Palette-style input prompts directly in VS Code, just like when
running terminal commands.

Key Features:
- Native VS Code input dialogs using FastMCP elicitations
- Simple, clean user interface that looks like VS Code's built-in prompts  
- Direct user input without complex JSON responses
- Support for text input, choices, confirmations, and info messages
- Compatible with VS Code Insiders MCP client

Usage:
python human_loop_server_v3.py

Author: Human-in-the-Loop MCP Server
Version: 3.0.0
Date: January 2025
"""

import asyncio
import logging
from typing import Optional, List, Literal
from dataclasses import dataclass
from enum import Enum

from fastmcp import FastMCP, Context

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create the FastMCP server
mcp = FastMCP("Human-in-the-Loop v3.0")

# Enums for choices
class InfoType(Enum):
    INFO = "info"
    WARNING = "warning" 
    ERROR = "error"
    SUCCESS = "success"

# =============================================================================
# CORE ELICITATION TOOLS - NATIVE VS CODE DIALOGS
# =============================================================================

@mcp.tool()
async def get_user_input(
    ctx: Context,
    prompt: str,
    title: Optional[str] = None,
    default_value: Optional[str] = None,
    input_type: Literal["text", "integer", "float"] = "text"
) -> str:
    """
    Get single-line input from user using native VS Code dialog.
    
    Creates a Command Palette-style input prompt directly in VS Code.
    User will see a native input field, not JSON responses.
    
    Args:
        prompt: The question/prompt to show the user
        title: Optional title for the input dialog  
        default_value: Optional default value to pre-fill
        input_type: Type of input expected (text, integer, float)
    
    Returns:
        The user's input as a string, or error message if cancelled
    """
    try:
        # Create the message for the user
        message = f"{title + ': ' if title else ''}{prompt}"
        if default_value:
            message += f" (default: {default_value})"
            
        # Use FastMCP elicitation to get native VS Code input dialog  
        if input_type == "integer":
            result = await ctx.elicit(message, response_type=int)
        elif input_type == "float":
            result = await ctx.elicit(message, response_type=float)
        else:
            result = await ctx.elicit(message, response_type=str)
        
        # Handle the response
        if result.action == "accept":
            return str(result.data)
        else:
            return f"User cancelled input request: {prompt}"
            
    except asyncio.TimeoutError:
        logger.warning(f"Timeout waiting for user input: {prompt}")
        return f"Timeout waiting for user input: {prompt}"
    except ConnectionError as e:
        logger.warning(f"Connection error during elicitation: {e}")
        return f"Connection interrupted while waiting for input: {prompt}"
    except Exception as e:
        logger.error(f"Error in get_user_input: {e}")
        return f"Error getting user input: {str(e)}"

@mcp.tool()
async def get_user_choice(
    ctx: Context,
    prompt: str,
    choices: List[str],
    title: Optional[str] = None,
    allow_multiple: bool = False
) -> str:
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
        # Create the message for the user
        message = f"{title + ': ' if title else ''}{prompt}"
        
        # Use FastMCP elicitation with choice list to get native VS Code choice picker
        result = await ctx.elicit(message, response_type=choices)
        
        # Handle the response
        if result.action == "accept":
            return f"User selected: {result.data}"
        else:
            return f"User cancelled choice request: {prompt}"
            
    except asyncio.TimeoutError:
        logger.warning(f"Timeout waiting for user choice: {prompt}")
        return f"Timeout waiting for user choice: {prompt}"
    except ConnectionError as e:
        logger.warning(f"Connection error during choice elicitation: {e}")
        return f"Connection interrupted while waiting for choice: {prompt}"
    except Exception as e:
        logger.error(f"Error in get_user_choice: {e}")
        return f"Error getting user choice: {str(e)}"

@mcp.tool()
async def get_multiline_input(
    ctx: Context,
    prompt: str,
    title: Optional[str] = None,
    placeholder: Optional[str] = None,
    default_value: Optional[str] = None
) -> str:
    """
    Get multi-line text input from user using native VS Code dialog.
    
    Creates a Command Palette-style text input directly in VS Code.
    User will see native text area, not JSON responses.
    
    Args:
        prompt: The question/prompt to show the user  
        title: Optional title for the input dialog
        placeholder: Optional placeholder text
        default_value: Optional default value to pre-fill
    
    Returns:
        The user's multiline input as a string, or error message if cancelled
    """
    try:
        # Create the message for the user
        message = f"{title + ': ' if title else ''}{prompt}"
        if placeholder:
            message += f" ({placeholder})"
        if default_value:
            message += f" [default: {default_value}]"
            
        # Use FastMCP elicitation to get native VS Code multiline input dialog
        result = await ctx.elicit(message, response_type=str)
        
        # Handle the response
        if result.action == "accept":
            return result.data
        else:
            return f"User cancelled multiline input request: {prompt}"
            
    except asyncio.TimeoutError:
        logger.warning(f"Timeout waiting for multiline input: {prompt}")
        return f"Timeout waiting for multiline input: {prompt}"
    except ConnectionError as e:
        logger.warning(f"Connection error during multiline input elicitation: {e}")
        return f"Connection interrupted while waiting for multiline input: {prompt}"
    except Exception as e:
        logger.error(f"Error in get_multiline_input: {e}")
        return f"Error getting multiline input: {str(e)}"

@mcp.tool()
async def show_confirmation_dialog(
    ctx: Context,
    message: str,
    title: Optional[str] = None,
    confirm_text: str = "Yes",
    cancel_text: str = "No"
) -> str:
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
        # Create the message for the user
        full_message = f"{title + ': ' if title else ''}{message}"
        
        # Use FastMCP elicitation to get native VS Code confirmation dialog
        result = await ctx.elicit(full_message, response_type=[confirm_text, cancel_text])
        
        # Handle the response
        if result.action == "accept":
            if result.data == confirm_text:
                return f"User confirmed: {message}"
            else:
                return f"User cancelled: {message}"
        else:
            return f"User cancelled confirmation request: {message}"
            
    except asyncio.TimeoutError:
        logger.warning(f"Timeout waiting for confirmation: {message}")
        return f"Timeout waiting for confirmation: {message}"
    except ConnectionError as e:
        logger.warning(f"Connection error during confirmation dialog: {e}")
        return f"Connection interrupted while waiting for confirmation: {message}"
    except Exception as e:
        logger.error(f"Error in show_confirmation_dialog: {e}")
        return f"Error showing confirmation dialog: {str(e)}"

@mcp.tool()
async def show_info_message(
    ctx: Context,
    message: str,
    title: Optional[str] = None,
    info_type: Literal["info", "warning", "error", "success"] = "info"
) -> str:
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
        # Create the message for the user
        prefix = {
            "info": "ℹ️ INFO",
            "warning": "⚠️ WARNING", 
            "error": "❌ ERROR",
            "success": "✅ SUCCESS"
        }.get(info_type, "ℹ️ INFO")
        
        full_message = f"{prefix}: {title + ' - ' if title else ''}{message}"
        
        # Use FastMCP elicitation to show native VS Code info dialog 
        result = await ctx.elicit(full_message, response_type=None)
        
        # Handle the response
        if result.action == "accept":
            return f"User acknowledged {info_type} message: {message}"
        else:
            return f"User cancelled {info_type} message: {message}"
            
    except asyncio.TimeoutError:
        logger.warning(f"Timeout showing info message: {message}")
        return f"Timeout showing info message: {message}"
    except ConnectionError as e:
        logger.warning(f"Connection error during info message: {e}")
        return f"Connection interrupted while showing info message: {message}"
    except Exception as e:
        logger.error(f"Error in show_info_message: {e}")
        return f"Error showing info message: {str(e)}"

@mcp.tool()
async def health_check(ctx: Context) -> str:
    """
    Check the health and status of the Human-in-the-Loop MCP Server v3.0.
    
    Returns comprehensive information about server capabilities,
    elicitation support, and operational status.
    
    Returns:
        Health check results and server information
    """
    try:
        health_info = {
            "status": "healthy",
            "version": "3.0.0",
            "description": "Human-in-the-Loop MCP Server with Native VS Code Elicitations",
            "capabilities": [
                "Native VS Code input dialogs via MCP elicitations",
                "Text input (single-line and multiline)", 
                "Multiple choice selection",
                "Confirmation dialogs",
                "Information messages",
                "Command Palette-style user interface"
            ],
            "elicitation_support": True,
            "mcp_version": "Compatible with MCP specification",
            "vs_code_integration": "Native Command Palette-style dialogs",
            "tools_available": [
                "get_user_input - Single-line text input",
                "get_user_choice - Multiple choice selection", 
                "get_multiline_input - Multi-line text input",
                "show_confirmation_dialog - Yes/No confirmations",
                "show_info_message - Information display",
                "health_check - Server status"
            ]
        }
        
        # Format the health info nicely
        health_report = "🚀 HUMAN-IN-THE-LOOP MCP SERVER v3.0 HEALTH CHECK\n\n"
        health_report += f"Status: {health_info['status'].upper()}\n"
        health_report += f"Version: {health_info['version']}\n"
        health_report += f"Description: {health_info['description']}\n\n"
        
        health_report += "✨ KEY FEATURES:\n"
        for capability in health_info['capabilities']:
            health_report += f"  • {capability}\n"
            
        health_report += f"\n🔗 MCP Integration:\n"
        health_report += f"  • Elicitation Support: {health_info['elicitation_support']}\n"
        health_report += f"  • MCP Version: {health_info['mcp_version']}\n"
        health_report += f"  • VS Code Integration: {health_info['vs_code_integration']}\n"
        
        health_report += f"\n🛠️ AVAILABLE TOOLS:\n"
        for tool in health_info['tools_available']:
            health_report += f"  • {tool}\n"
            
        health_report += f"\n💡 USAGE:\n"
        health_report += f"  This server creates NATIVE VS Code input dialogs!\n"
        health_report += f"  When you use these tools, you'll see Command Palette-style\n"
        health_report += f"  prompts directly in VS Code, not JSON responses.\n"
        
        return health_report
        
    except Exception as e:
        logger.error(f"Error in health_check: {e}")
        return f"Health check failed: {str(e)}"

# =============================================================================
# SERVER LIFECYCLE
# =============================================================================

def main():
    """Main entry point for the Human-in-the-Loop MCP Server v3.0"""
    try:
        logger.info("🚀 Starting Human-in-the-Loop MCP Server v3.0")
        logger.info("📱 This server creates NATIVE VS Code input dialogs using MCP elicitations")
        logger.info("🎯 Users will see Command Palette-style prompts, not JSON responses")
        
        # Start the server
        mcp.run()
        
    except KeyboardInterrupt:
        logger.info("👋 Server stopped by user")
    except Exception as e:
        logger.error(f"❌ Server error: {e}")
        raise

if __name__ == "__main__":
    main()
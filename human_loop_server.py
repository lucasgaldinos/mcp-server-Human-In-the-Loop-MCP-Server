#!/usr/bin/env python3
"""
Human-in-the-Loop MCP Server

This server provides tools for getting human input and choices through GUI dialogs.
It enables LLMs to pause and ask for human feedback, input, or decisions.
Supports Windows, macOS, and Linux platforms.
"""

import os
import platform

# Set required environment variable for FastMCP 2.8.1+
os.environ.setdefault('FASTMCP_LOG_LEVEL', 'INFO')

from fastmcp import FastMCP
from src.human_in_the_loop.tools import register_tools, register_prompts
from src.human_in_the_loop.utils.platform import (
    CURRENT_PLATFORM, IS_WINDOWS, IS_MACOS, IS_LINUX
)
from src.human_in_the_loop.utils.gui import ensure_gui_initialized


# Initialize the MCP server
mcp = FastMCP("Human-in-the-Loop Server")

# Register all tools and prompts
register_tools(mcp)
register_prompts(mcp)


def main():
    """Main entry point for the Human-in-the-Loop MCP Server."""
    print("Starting Human-in-the-Loop MCP Server...")
    print("This server provides tools for LLMs to interact with humans through GUI dialogs.")
    print(f"Platform: {CURRENT_PLATFORM} ({platform.system()} {platform.release()})")
    print("")
    print("Available tools:")
    print("  get_user_input - Get text/number input from user")
    print("  get_user_choice - Let user choose from options")
    print("  get_multiline_input - Get multi-line text from user")
    print("  show_confirmation_dialog - Ask user for yes/no confirmation")
    print("  show_info_message - Display information to user")
    print("  health_check - Check server status")
    print("")
    print("Available prompts:")
    print("  get_human_loop_prompt - Get guidance on when to use human-in-the-loop tools")
    print("")
    
    # Platform-specific startup messages
    if IS_MACOS:
        print("macOS detected - Using native system fonts and window management")
        print("Note: You may need to allow Python to control your computer in System Preferences > Security & Privacy > Accessibility")
    elif IS_WINDOWS:
        print("Windows detected - Using modern Windows 11-style GUI with enhanced styling")
        print("Features: Modern colors, improved fonts, hover effects, and sleek design")
    elif IS_LINUX:
        print("Linux detected - Using Linux-compatible GUI settings with modern styling")
    
    # Test GUI availability
    if ensure_gui_initialized():
        print("✓ GUI system initialized successfully")
        if IS_MACOS:
            print("  macOS GUI optimizations applied")
    else:
        print("⚠ Warning: GUI system may not be available")
    
    print("")
    print("Starting MCP server...")
    
    # Run the server
    mcp.run()


if __name__ == "__main__":
    main()

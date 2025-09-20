#!/usr/bin/env python3
"""Test our prompt functions directly to understand structure."""

import sys
sys.path.insert(0, 'src')

from fastmcp import FastMCP
from human_in_the_loop.prompts.user_prompts import register_prompts

def test_prompt_structure():
    """Test our prompt implementation directly."""
    # Create a temporary MCP instance to register prompts
    mcp = FastMCP("test-server")
    register_prompts(mcp)
    
    print("Prompts registered successfully!")
    print("Available prompts:", list(mcp._prompts.keys()))
    
    # Check if we can access a prompt function directly
    if 'get_user_input_prompt' in mcp._prompts:
        prompt_func = mcp._prompts['get_user_input_prompt']
        print("Found get_user_input_prompt function:", prompt_func)

if __name__ == "__main__":
    test_prompt_structure()
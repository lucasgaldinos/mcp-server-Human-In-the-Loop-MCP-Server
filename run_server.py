#!/usr/bin/env python3
"""
Entry point for the Human-in-the-Loop MCP Server v4.1

This script provides a clean entry point for running the server.
"""

import sys
import os

# Add src directory to Python path to allow imports
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir, "src")
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

from human_in_the_loop_mcp import main

if __name__ == "__main__":
    main()
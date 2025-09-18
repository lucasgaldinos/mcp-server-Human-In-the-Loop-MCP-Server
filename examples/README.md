# Human-in-the-Loop MCP Server Examples

This directory contains examples of how to use the Human-in-the-Loop MCP Server.

## Basic Usage Example

```python
#!/usr/bin/env python3
"""
Example of using Human-in-the-Loop MCP Server programmatically.

This example shows how to initialize and test the server components.
"""

from src.human_in_the_loop.utils.platform import get_platform_info
from src.human_in_the_loop.utils.gui import test_gui_availability
from src.human_in_the_loop.dialogs import InputDialog

def main():
    # Check platform
    platform_info = get_platform_info()
    print(f"Platform: {platform_info['system']} {platform_info['release']}")
    
    # Test GUI availability
    gui_status = test_gui_availability()
    print(f"GUI Available: {gui_status['gui_available']}")
    
    if gui_status['gui_available']:
        # Example of creating a dialog (in a real GUI environment)
        print("GUI is available - dialogs can be created")
    else:
        print("GUI not available - running in headless mode")

if __name__ == "__main__":
    main()
```

## VS Code Integration Example

To integrate with VS Code as an MCP server, add this to your VS Code settings:

```json
{
  "mcp.servers": {
    "human-in-the-loop": {
      "command": "python",
      "args": ["/path/to/human_loop_server.py"],
      "cwd": "/path/to/mcp-server-Human-In-the-Loop-MCP-Server"
    }
  }
}
```

## Available Tools

### get_user_input

Get single-line text or number input from the user.

**Parameters:**

- `title`: Dialog window title
- `prompt`: Question to show the user
- `input_type`: "text", "integer", or "float"
- `default_value`: Pre-filled default value

**Example usage in MCP client:**

```python
result = await client.call_tool("get_user_input", {
    "title": "Configuration",
    "prompt": "Enter your API key:",
    "input_type": "text"
})
```

### get_user_choice

Let the user select from multiple options.

**Parameters:**

- `title`: Dialog window title
- `prompt`: Question to show the user
- `choices`: List of options to choose from
- `allow_multiple`: Whether to allow multiple selections

**Example:**

```python
result = await client.call_tool("get_user_choice", {
    "title": "Select Framework",
    "prompt": "Which framework would you like to use?",
    "choices": ["React", "Vue", "Angular", "Vanilla JS"],
    "allow_multiple": false
})
```

### get_multiline_input

Get multi-line text input from the user.

**Parameters:**

- `title`: Dialog window title
- `prompt`: Question to show the user
- `default_value`: Pre-filled text

**Example:**

```python
result = await client.call_tool("get_multiline_input", {
    "title": "Code Review",
    "prompt": "Please provide your feedback on the code:",
    "default_value": "The code looks good overall, but..."
})
```

### show_confirmation_dialog

Ask for yes/no confirmation.

**Parameters:**

- `title`: Dialog window title
- `message`: Message to display

**Example:**

```python
result = await client.call_tool("show_confirmation_dialog", {
    "title": "Confirm Action",
    "message": "Are you sure you want to delete these 15 files?"
})
```

### show_info_message

Display information to the user.

**Parameters:**

- `title`: Dialog window title
- `message`: Information to display

**Example:**

```python
result = await client.call_tool("show_info_message", {
    "title": "Process Complete",
    "message": "Successfully processed 1,250 records."
})
```

### health_check

Check server status and GUI availability.

**Example:**

```python
result = await client.call_tool("health_check", {})
print(f"Server status: {result['status']}")
print(f"GUI available: {result['gui_available']}")
```

## Prompts

### get_human_loop_prompt

Get comprehensive guidance on when and how to use human-in-the-loop tools.

This prompt provides LLMs with detailed guidance on:

- When to use human-in-the-loop tools
- Best practices for user interaction
- Decision frameworks for tool selection
- Integration tips and examples

**Example:**

```python
guidance = await client.call_prompt("get_human_loop_prompt", {})
print(guidance['main_prompt'])
```

## Error Handling

All tools return structured responses with error information:

```python
{
    "success": True,
    "result": "user input here",
    "error": None
}
```

Or in case of error:

```python
{
    "success": False,
    "result": None,
    "error": "Error description"
}
```

## Platform-Specific Notes

### Windows

- Uses modern Windows 11-style GUI
- Supports hover effects and modern styling
- May require GUI libraries to be installed

### macOS

- Uses native SF Pro Display fonts
- May require accessibility permissions for Python
- Supports native window management

### Linux

- Uses system-appropriate fonts (Ubuntu/monospace)
- Requires X11 or Wayland display server
- May need additional GUI packages installed

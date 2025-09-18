# Setup Documentation

This directory contains documentation for the Human-in-the-Loop MCP Server.

## Quick Setup

1. **Install dependencies:**
   ```bash
   uv sync
   ```

2. **Run the server:**
   ```bash
   uv run python human_loop_server.py
   ```

3. **Test the server:**
   ```bash
   uv run python -m pytest tests/
   ```

## Available Documentation

- [Context](CONTEXT.md) - Architectural decisions and design rationale
- [Tasks](tasks/TASKS.md) - Detailed task breakdown and progress tracking
- [Tree of Thoughts](ToT/) - Decision-making analysis for project structure

## Integration with VS Code

To use this server with VS Code and MCP clients:

1. Add the server configuration to your MCP client settings
2. The server provides the following tools:
   - `get_user_input` - Single-line text/number input
   - `get_user_choice` - Multiple choice selection
   - `get_multiline_input` - Multi-line text input
   - `show_confirmation_dialog` - Yes/no confirmations
   - `show_info_message` - Information display
   - `health_check` - Server status monitoring

3. The server also provides guidance prompts:
   - `get_human_loop_prompt` - Comprehensive guidance on when and how to use human-in-the-loop tools

## Architecture

The project follows modern Python packaging standards with a modular structure:

```
src/human_in_the_loop/
├── __init__.py           # Package initialization
├── dialogs/              # GUI dialog implementations  
│   ├── __init__.py
│   ├── base.py          # Base dialog class
│   ├── input.py         # Text input dialogs
│   ├── choice.py        # Choice selection dialogs
│   ├── multiline.py     # Multi-line text input
│   ├── confirmation.py  # Yes/no confirmation dialogs
│   └── info.py          # Information display dialogs
├── tools/               # MCP tool definitions
│   ├── __init__.py
│   ├── dialog_tools.py  # FastMCP tool registration
│   └── prompts.py       # LLM guidance prompts
└── utils/               # Cross-platform utilities
    ├── __init__.py
    ├── platform.py      # Platform detection
    ├── styling.py       # GUI styling and theming
    └── gui.py           # GUI initialization
```

## Platform Support

- **Windows**: Modern Windows 11-style GUI with enhanced styling
- **macOS**: Native system fonts and window management
- **Linux**: Linux-compatible GUI settings with modern styling

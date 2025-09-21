# Human-in-the-Loop MCP Server# Human-in-the-Loop MCP Server# Human-In-the-Loop MCP Server

> **🎯 Current Version: v4.1 Clean Implementation**

>

> A production-ready Model Context Protocol server providing 5 essential human interaction tools through VS Code's native Command Palette interface.> **🎯 Current Version: v4.1 Clean Implementation**![](https://badge.mcpx.dev?type=server 'MCP Server')

## Quick Start> [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

1. **Install dependencies:**> A production-ready Model Context Protocol server providing 5 essential human interaction tools through VS Code's native Command Palette interface.[![PyPI version](https://badge.fury.io/py/hitl-mcp-server.svg)](https://badge.fury.io/py/hitl-mcp-server)

   ```bash

   uv sync

   ```## Quick StartA powerful **Model Context Protocol (MCP) Server** that enables AI assistants like Claude to interact with humans through intuitive GUI dialogs. This server bridges the gap between automated AI processes and human decision-making by providing real-time user input tools, choices, confirmations, and feedback mechanisms.



2. **Configure VS Code MCP client** (`.vscode/mcp.json`):

   ```json1. **Install dependencies:**![demo](demo.gif)

   {

     "servers": {   ```bash

       "human-in-the-loop-clean": {

         "command": "uv",   uv sync## 🚀 Features

         "args": ["run", "python", "run_server.py"],

         "cwd": "/path/to/this/repository",   ```

         "type": "stdio"

       }### 💬 Interactive Dialog Tools

     }

   }2. **Configure VS Code MCP client** (`.vscode/mcp.json`):- **Text Input**: Get text, numbers, or other data from users with validation

   ```

   ```json- **Multiple Choice**: Present options for single or multiple selections  

3. **Restart VS Code** to load the MCP server

   {- **Multi-line Input**: Collect longer text content, code, or detailed descriptions

## What This Server Does

     "servers": {- **Confirmation Dialogs**: Ask for yes/no decisions before proceeding with actions

✅ **5 Working Tools**:

       "human-in-the-loop-clean": {- **Information Messages**: Display notifications, status updates, and results

- `get_user_input` - Single-line text/number input

- `get_user_choice` - Multiple choice selection           "command": "uv",- **Health Check**: Monitor server status and GUI availability

- `show_confirmation_dialog` - Yes/No confirmations

- `show_info_message` - Information display         "args": ["run", "python", "run_server.py"],

- `health_check` - Server status

         "cwd": "/path/to/this/repository",### 🎨 Modern Cross-Platform GUI

❌ **What it doesn't do**: Multiline text editing (MCP protocol limitation)

         "type": "stdio"- **Windows**: Modern Windows 11-style interface with beautiful styling, hover effects, and enhanced visual design

## Documentation

       }- **macOS**: Native macOS experience with SF Pro Display fonts and proper window management

- **📖 [Complete Documentation](README_V4_1_CLEAN.md)** - Full usage guide and API reference

- **📋 [Implementation Summary](docs/V4_1_FINAL_SUMMARY.md)** - Technical details and architecture     }- **Linux**: Ubuntu-compatible GUI with modern styling and system fonts

- **🏗️ [Project Structure](#project-structure)** - How this repository is organized

   }

## Project Structure

   ```### ⚡ Advanced Features

```

├── src/human_in_the_loop_mcp/    # Main package- **Non-blocking Operation**: All dialogs run in separate threads to prevent blocking

│   ├── **init**.py               # Package initialization

│   └── server.py                 # Clean v4.1 server implementation3. **Restart VS Code** to load the MCP server- **Timeout Protection**: Configurable 5-minute timeouts prevent hanging operations

├── run_server.py                 # Entry point script

├── tests/                        # Test suite- **Platform Detection**: Automatic optimization for each operating system

│   ├── unit/                     # Unit tests

│   └── integration/              # Integration tests## What This Server Does- **Modern UI Design**: Beautiful interface with smooth animations and hover effects

├── examples/                     # Usage examples and demos

├── docs/                         # Documentation- **Error Handling**: Comprehensive error reporting and graceful recovery

├── legacy/                       # Previous server versions (reference)

├── archive/                      # Archived files and old documentation✅ **5 Working Tools**:- **Keyboard Navigation**: Full keyboard shortcuts support (Enter/Escape)

├── .vscode/mcp.json              # VS Code MCP configuration

└── README_V4_1_CLEAN.md          # Complete documentation- `get_user_input` - Single-line text/number input

```

- `get_user_choice` - Multiple choice selection  ## 📦 Installation & Setup

## Version History

- `show_confirmation_dialog` - Yes/No confirmations

- **v4.1** ✅ - Clean implementation (current)

- **v4.0** ❌ - Over-engineered (removed)  - `show_info_message` - Information display### Quick Install with uvx (Recommended)

- **v3.0** 📚 - Legacy working version (in `/legacy/`)

- `health_check` - Server status

## Why This Approach?

The easiest way to use this MCP server is with `uvx`:

This server focuses on **simplicity and reliability**:

❌ **What it doesn't do**: Multiline text editing (MCP protocol limitation)

- ✅ **Honest limitations** - Documents what actually works

- ✅ **Native integration** - Uses VS Code's Command Palette```bash

- ✅ **Clean codebase** - Easy to understand and maintain

- ✅ **Production ready** - Comprehensive error handling## Documentation# Install and run directly



## Contributinguvx hitl-mcp-server



This project prioritizes working solutions over complex workarounds. See [the complete documentation](README_V4_1_CLEAN.md) for technical details.- **📖 [Complete Documentation](README_V4_1_CLEAN.md)** - Full usage guide and API reference



## License- **📋 [Implementation Summary](docs/V4_1_FINAL_SUMMARY.md)** - Technical details and architecture# Or use the underscore version



MIT License - See [LICENSE](LICENSE) file for details- **🏗️ [Project Structure](#project-structure)** - How this repository is organizeduvx hitl_mcp_server

```

## Project Structure

### Manual Installation

```

├── src/human_in_the_loop_mcp/    # Main package1. **Install from PyPI**:

│   ├── __init__.py               # Package initialization   ```bash

│   └── server.py                 # Clean v4.1 server implementation   pip install hitl-mcp-server

├── run_server.py                 # Entry point script   ```

├── tests/                        # Test suite

│   ├── unit/                     # Unit tests2. **Run the server**:

│   └── integration/              # Integration tests   ```bash

├── examples/                     # Usage examples and demos   hitl-mcp-server

├── docs/                         # Documentation   # or

├── legacy/                       # Previous server versions (reference)   hitl_mcp_server

├── archive/                      # Archived files and old documentation   ```

├── .vscode/mcp.json              # VS Code MCP configuration

└── README_V4_1_CLEAN.md          # Complete documentation### Development Installation

```

1. **Clone the repository**:

## Version History   ```bash

   git clone <https://github.com/GongRzhe/Human-In-the-Loop-MCP-Server.git>

- **v4.1** ✅ - Clean implementation (current)   cd Human-In-the-Loop-MCP-Server

- **v4.0** ❌ - Over-engineered (removed)     ```

- **v3.0** 📚 - Legacy working version (in `/legacy/`)

2. **Install in development mode**:

## Why This Approach?   ```bash

   pip install -e .

This server focuses on **simplicity and reliability**:   ```

- ✅ **Honest limitations** - Documents what actually works## 🔧 Claude Desktop Configuration

- ✅ **Native integration** - Uses VS Code's Command Palette

- ✅ **Clean codebase** - Easy to understand and maintainTo use this server with Claude Desktop, add the following configuration to your `claude_desktop_config.json`:

- ✅ **Production ready** - Comprehensive error handling

### Using uvx (Recommended)

## Contributing

```json

This project prioritizes working solutions over complex workarounds. See [the complete documentation](README_V4_1_CLEAN.md) for technical details.{

  "mcpServers": {

## License    "human-in-the-loop": {

      "command": "uvx",

MIT License - See [LICENSE](LICENSE) file for details      "args": ["hitl-mcp-server"]
    }
  }
}
```

### Using pip installation

```json
{
  "mcpServers": {
    "human-in-the-loop": {
      "command": "hitl-mcp-server",
      "args": []
    }
  }
}
```

### Configuration File Locations

- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Linux**: `~/.config/Claude/claude_desktop_config.json`

### Important Note for macOS Users

**Note:** You may need to allow Python to control your computer in **System Preferences > Security & Privacy > Accessibility** for the GUI dialogs to work properly.

After updating the configuration, restart Claude Desktop for the changes to take effect.

## 🛠️ Available Tools

### 1. `get_user_input`

Get single-line text, numbers, or other data from users.

**Parameters:**

- `title` (str): Dialog window title
- `prompt` (str): Question/prompt text  
- `default_value` (str): Pre-filled value (optional)
- `input_type` (str): "text", "integer", or "float" (default: "text")

**Example Usage:**

```python
result = await get_user_input(
    title="Project Setup",
    prompt="Enter your project name:",
    default_value="my-project",
    input_type="text"
)
```

### 2. `get_user_choice`

Present multiple options for user selection.

**Parameters:**

- `title` (str): Dialog window title
- `prompt` (str): Question/prompt text
- `choices` (List[str]): Available options
- `allow_multiple` (bool): Allow multiple selections (default: false)

**Example Usage:**

```python
result = await get_user_choice(
    title="Framework Selection",
    prompt="Choose your preferred framework:",
    choices=["React", "Vue", "Angular", "Svelte"],
    allow_multiple=False
)
```

### 3. `get_multiline_input`

Collect longer text content, code, or detailed descriptions.

**Parameters:**

- `title` (str): Dialog window title
- `prompt` (str): Question/prompt text
- `default_value` (str): Pre-filled text (optional)

**Example Usage:**

```python
result = await get_multiline_input(
    title="Code Review",
    prompt="Please provide your detailed feedback:",
    default_value=""
)
```

### 4. `show_confirmation_dialog`

Ask for yes/no confirmation before proceeding.

**Parameters:**

- `title` (str): Dialog window title
- `message` (str): Confirmation message

**Example Usage:**

```python
result = await show_confirmation_dialog(
    title="Delete Confirmation",
    message="Are you sure you want to delete these 5 files? This action cannot be undone."
)
```

### 5. `show_info_message`

Display information, notifications, or status updates.

**Parameters:**

- `title` (str): Dialog window title
- `message` (str): Information message

**Example Usage:**

```python
result = await show_info_message(
    title="Process Complete",
    message="Successfully processed 1,247 records in 2.3 seconds!"
)
```

### 6. `health_check`

Check server status and GUI availability.

**Example Usage:**

```python
status = await health_check()
# Returns detailed platform and functionality information
```

## 📋 Response Format

All tools return structured JSON responses:

```json
{
    "success": true,
    "user_input": "User's response text",
    "cancelled": false,
    "platform": "windows",
    "input_type": "text"
}
```

**Common Response Fields:**

- `success` (bool): Whether the operation completed successfully
- `cancelled` (bool): Whether the user cancelled the dialog
- `platform` (str): Operating system platform
- `error` (str): Error message if operation failed

**Tool-Specific Fields:**

- **get_user_input**: `user_input`, `input_type`
- **get_user_choice**: `selected_choice`, `selected_choices`, `allow_multiple`
- **get_multiline_input**: `user_input`, `character_count`, `line_count`
- **show_confirmation_dialog**: `confirmed`, `response`
- **show_info_message**: `acknowledged`

## 🧠 Best Practices for AI Integration

### When to Use Human-in-the-Loop Tools

1. **Ambiguous Requirements** - When user instructions are unclear
2. **Decision Points** - When you need user preference between valid alternatives
3. **Creative Input** - For subjective choices like design or content style
4. **Sensitive Operations** - Before executing potentially destructive actions
5. **Missing Information** - When you need specific details not provided
6. **Quality Feedback** - To get user validation on intermediate results

### Example Integration Patterns

#### File Operations

```python
# Get target directory
location = await get_user_input(
    title="Backup Location",
    prompt="Enter backup directory path:",
    default_value="~/backups"
)

# Choose backup type
backup_type = await get_user_choice(
    title="Backup Options",
    prompt="Select backup type:",
    choices=["Full Backup", "Incremental", "Differential"]
)

# Confirm before proceeding
confirmed = await show_confirmation_dialog(
    title="Confirm Backup",
    message=f"Create {backup_type['selected_choice']} backup to {location['user_input']}?"
)

if confirmed['confirmed']:
    # Perform backup
    await show_info_message("Success", "Backup completed successfully!")
```

#### Content Creation

```python
# Get content requirements
requirements = await get_multiline_input(
    title="Content Requirements",
    prompt="Describe your content requirements in detail:"
)

# Choose tone and style
tone = await get_user_choice(
    title="Content Style",
    prompt="Select desired tone:",
    choices=["Professional", "Casual", "Friendly", "Technical"]
)

# Generate and show results
# ... content generation logic ...
await show_info_message("Content Ready", "Your content has been generated successfully!")
```

## 🔍 Troubleshooting

### Common Issues

**GUI Not Appearing**

- Verify you're running in a desktop environment (not headless server)
- Check if tkinter is installed: `python -c "import tkinter"`
- Run health check: `health_check()` tool to diagnose issues

**Permission Errors (macOS)**

- Grant accessibility permissions in System Preferences > Security & Privacy > Accessibility
- Allow Python to control your computer
- Restart terminal after granting permissions

**Import Errors**

- Ensure package is installed: `pip install hitl-mcp-server`
- Check Python version compatibility (>=3.8 required)
- Verify virtual environment activation if using one

**Claude Desktop Integration Issues**

- Check configuration file syntax and location
- Restart Claude Desktop after configuration changes
- Verify uvx is installed: `pip install uvx`
- Test server manually: `uvx hitl-mcp-server`

**Dialog Timeout**

- Default timeout is 5 minutes (300 seconds)
- Dialogs will return with cancelled=true if user doesn't respond
- Ensure user is present when dialogs are triggered

### Debug Mode

Enable detailed logging by running the server with environment variable:

```bash
HITL_DEBUG=1 uvx hitl-mcp-server
```

## 🏗️ Development

### Project Structure

```
Human-In-the-Loop-MCP-Server/
├── human_loop_server.py       # Main server implementation
├── pyproject.toml            # Package configuration
├── README.md                 # Documentation
├── LICENSE                   # MIT License
├── .gitignore               # Git ignore rules
└── demo.gif                 # Demo animation
```

### Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes with proper testing
4. Follow code style guidelines (Black, Ruff)
5. Add type hints and docstrings
6. Submit a pull request with detailed description

### Code Quality

- **Formatting**: Black (line length: 88)
- **Linting**: Ruff with comprehensive rule set
- **Type Checking**: MyPy with strict configuration
- **Testing**: Pytest for unit and integration tests

## 🌍 Platform Support

### Windows

- Windows 10/11 with modern UI styling
- Enhanced visual design with hover effects
- Segoe UI and Consolas font integration
- Full keyboard navigation support

### macOS

- Native macOS experience
- SF Pro Display system fonts
- Proper window management and focus
- Accessibility permission handling

### Linux

- Ubuntu/Debian compatible
- Modern styling with system fonts
- Cross-distribution GUI support
- Minimal dependency requirements

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Acknowledgments

- Built with [FastMCP](https://github.com/jlowin/fastmcp) framework
- Uses [Pydantic](https://pydantic-docs.helpmanual.io/) for data validation
- Cross-platform GUI powered by tkinter
- Inspired by the need for human-AI collaboration

## 🔗 Links

- **PyPI Package**: [https://pypi.org/project/hitl-mcp-server/](https://pypi.org/project/hitl-mcp-server/)
- **Repository**: [https://github.com/GongRzhe/Human-In-the-Loop-MCP-Server](https://github.com/GongRzhe/Human-In-the-Loop-MCP-Server)
- **Issues**: [Report bugs or request features](https://github.com/GongRzhe/Human-In-the-Loop-MCP-Server/issues)
- **MCP Protocol**: [Learn about Model Context Protocol](https://modelcontextprotocol.io/)

## 📊 Usage Statistics

- **Cross-Platform**: Windows, macOS, Linux
- **Python Support**: 3.8, 3.9, 3.10, 3.11, 3.12+
- **GUI Framework**: tkinter (built-in with Python)
- **Thread Safety**: Full concurrent operation support
- **Response Time**: < 100ms dialog initialization
- **Memory Usage**: < 50MB typical operation

---

**Made with ❤️ for the AI community - Bridging humans and AI through intuitive interaction**

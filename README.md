# Human-In-the-Loop MCP Server

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Platform Support](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey)](https://github.com/GongRzhe/Human-In-the-Loop-MCP-Server)

A powerful **Model Context Protocol (MCP) Server** that enables AI assistants to interact with humans through intuitive GUI dialogs. This server bridges the gap between automated AI processes and human decision-making by providing tools for real-time user input, choices, confirmations, and feedback.

## 🚀 Features

### 💬 Interactive Dialog Tools
- **Text Input**: Get text, numbers, or other data from users
- **Multiple Choice**: Present options for single or multiple selections  
- **Multi-line Input**: Collect longer text content, code, or detailed descriptions
- **Confirmation Dialogs**: Ask for yes/no decisions before proceeding
- **Information Messages**: Display notifications and status updates

### 🖥️ Cross-Platform Support
- **Windows**: Native Windows GUI with Segoe UI fonts
- **macOS**: Native macOS experience with SF Pro Display fonts and proper window management
- **Linux**: Ubuntu-compatible GUI with system fonts

### ⚡ Advanced Features
- **Non-blocking Operation**: All dialogs run in separate threads
- **Timeout Protection**: Configurable timeouts prevent hanging
- **Platform Detection**: Automatic optimization for each operating system
- **Error Handling**: Comprehensive error reporting and recovery
- **Health Monitoring**: Built-in health check and status reporting

## 📦 Installation

### Prerequisites
- Python 3.8 or higher
- tkinter (usually included with Python)
- pip package manager

### Quick Start

1. **Clone the repository**:
   ```bash
   git clone https://github.com/GongRzhe/Human-In-the-Loop-MCP-Server.git
   cd Human-In-the-Loop-MCP-Server
   ```

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv .venv
   
   # Windows
   .venv\Scripts\activate
   
   # macOS/Linux
   source .venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install fastmcp pydantic
   ```

4. **Run the server**:
   ```bash
   python human_loop_server.py
   ```

### Platform-Specific Setup

#### macOS
- Grant Python accessibility permissions in **System Preferences > Security & Privacy > Accessibility**
- This allows proper window focus and app activation

#### Windows
- No additional setup required
- Windows Defender may prompt for network access permission

#### Linux
- Ensure tkinter is installed: `sudo apt-get install python3-tk` (Ubuntu/Debian)
- Some distributions may require additional GUI libraries

## 🛠️ Usage

### Basic Integration

The server provides several MCP tools that can be used by AI assistants:

#### Get User Input
```python
# Request text input from user
result = await get_user_input(
    title="User Information",
    prompt="Please enter your name:",
    default_value="",
    input_type="text"
)
```

#### Get User Choice
```python
# Present multiple options
result = await get_user_choice(
    title="Select Option",
    prompt="Choose your preferred programming language:",
    choices=["Python", "JavaScript", "Java", "C++"],
    allow_multiple=False
)
```

#### Multi-line Input
```python
# Collect longer text content
result = await get_multiline_input(
    title="Code Review",
    prompt="Please provide your code review comments:",
    default_value=""
)
```

#### Confirmation Dialog
```python
# Ask for confirmation
result = await show_confirmation_dialog(
    title="Confirm Action",
    message="Are you sure you want to delete this file?"
)
```

#### Information Message
```python
# Display information
result = await show_info_message(
    title="Process Complete",
    message="Your file has been successfully processed!"
)
```

### Response Format

All tools return structured responses:

```json
{
    "success": true,
    "user_input": "User's response",
    "cancelled": false,
    "platform": "darwin",
    "input_type": "text"
}
```

### Health Check

Monitor server status:

```python
status = await health_check()
# Returns detailed platform and status information
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `HILMCP_TIMEOUT` | Dialog timeout in seconds | 300 |
| `HILMCP_FONT_SIZE` | UI font size | Platform-specific |

### Customization

You can modify the server by:

1. **Changing Fonts**: Edit `get_system_font()` function
2. **Window Sizes**: Modify geometry settings in dialog classes
3. **Timeouts**: Adjust timeout values in tool functions
4. **Platform Behavior**: Customize platform-specific configurations

## 📋 API Reference

### Tools

| Tool | Description |
|------|-------------|
| `get_user_input` | Single-line text/number input |
| `get_user_choice` | Multiple choice selection |
| `get_multiline_input` | Multi-line text input |
| `show_confirmation_dialog` | Yes/No confirmation |
| `show_info_message` | Information display |
| `health_check` | Server status check |

### Parameters

#### get_user_input
- `title` (str): Dialog window title
- `prompt` (str): Question/prompt text
- `default_value` (str): Pre-filled value
- `input_type` (str): "text", "integer", or "float"

#### get_user_choice
- `title` (str): Dialog window title
- `prompt` (str): Question/prompt text
- `choices` (List[str]): Available options
- `allow_multiple` (bool): Allow multiple selections

#### get_multiline_input
- `title` (str): Dialog window title
- `prompt` (str): Question/prompt text
- `default_value` (str): Pre-filled text

#### show_confirmation_dialog
- `title` (str): Dialog window title
- `message` (str): Confirmation message

#### show_info_message
- `title` (str): Dialog window title
- `message` (str): Information message

## 🔍 Troubleshooting

### Common Issues

**GUI Not Appearing**
- Check if GUI environment is available
- Verify tkinter installation
- Run health check to diagnose issues

**Permission Errors (macOS)**
- Grant accessibility permissions in System Preferences
- Restart terminal after granting permissions

**Import Errors**
- Ensure virtual environment is activated
- Install dependencies: `pip install fastmcp pydantic`

**Dialog Timeout**
- Increase timeout value in environment variables
- Check if user interaction is required

### Debug Mode

Enable debug logging:
```bash
python human_loop_server.py --debug
```

## 🏗️ Development

### Project Structure
```
Human-In-the-Loop-MCP-Server/
├── human_loop_server.py    # Main server implementation
├── .gitignore             # Git ignore file
├── .venv/                 # Virtual environment
└── README.md              # This file
```

### Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes
4. Add tests if applicable
5. Commit your changes: `git commit -am 'Add feature'`
6. Push to the branch: `git push origin feature-name`
7. Submit a pull request

### Code Style

- Follow PEP 8 guidelines
- Use type hints
- Add docstrings for functions and classes
- Include error handling

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Acknowledgments

- Built with [FastMCP](https://github.com/jlowin/fastmcp) framework
- Uses [Pydantic](https://pydantic-docs.helpmanual.io/) for data validation
- Cross-platform GUI powered by tkinter

## 🔗 Links

- **Repository**: [https://github.com/GongRzhe/Human-In-the-Loop-MCP-Server](https://github.com/GongRzhe/Human-In-the-Loop-MCP-Server)
- **Issues**: [Report bugs or request features](https://github.com/GongRzhe/Human-In-the-Loop-MCP-Server/issues)
- **MCP Protocol**: [Learn about Model Context Protocol](https://modelcontextprotocol.io/)

## 📊 Usage Examples

### Example 1: Collecting User Preferences
```python
# Get user's preferred settings
preferences = await get_user_choice(
    title="Setup Preferences",
    prompt="Select your preferred theme:",
    choices=["Dark", "Light", "Auto"],
    allow_multiple=False
)

# Configure based on user choice
if preferences["selected_choice"] == "Dark":
    apply_dark_theme()
```

### Example 2: Code Review Workflow
```python
# Get code for review
code = await get_multiline_input(
    title="Code Review",
    prompt="Paste the code you want reviewed:",
    default_value=""
)

# Process the code
analysis = analyze_code(code["user_input"])

# Show results
await show_info_message(
    title="Review Complete",
    message=f"Analysis complete. Found {len(analysis.issues)} issues."
)
```

### Example 3: Confirmation Before Action
```python
# Confirm before destructive action
confirmation = await show_confirmation_dialog(
    title="Delete Confirmation",
    message="This will permanently delete all selected files. Continue?"
)

if confirmation["confirmed"]:
    delete_files()
    await show_info_message("Success", "Files deleted successfully!")
else:
    await show_info_message("Cancelled", "Operation cancelled by user.")
```

---

**Made with ❤️ for the AI community**
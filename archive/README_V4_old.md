# Human-in-the-Loop MCP Server v4.0 - Advanced Interaction Patterns

## 🚀 What's New in v4.0

Version 4.0 implements **multiple MCP interaction patterns** to overcome the limitations of elicitations and provide optimal user experiences for different types of input:

### 🎯 **Key Innovation: True Multiline Input**

Finally solved the multiline input limitation! v4.0 provides **real multiline editing** through VS Code's native editor, not limited to single-line Command Palette inputs.

## 📋 Interaction Patterns

### 1. **Elicitations** (Simple Inputs)

*Native VS Code Command Palette dialogs*

**Best for:** Single-line text, choices, confirmations  
**Tools:** `get_user_input`, `get_user_choice`, `show_confirmation_dialog`, `show_info_message`

```python
# Single-line text input
result = await get_user_input(prompt="Enter your name")

# Multiple choice selection  
choice = await get_user_choice(prompt="Choose color", choices=["red", "blue", "green"])

# Yes/No confirmation
confirmed = await show_confirmation_dialog(message="Save changes?")
```

### 2. **Resources** (True Multiline Editing) ⭐ **NEW**

*VS Code resource browser with full editor capabilities*

**Best for:** Multiline text, documentation, code snippets  
**Tools:** `create_text_editor`, `get_text_content`

```python
# Create editable text resource
editor = await create_text_editor(purpose="meeting notes", initial_text="# Meeting Notes\n\n")

# User edits via: MCP: Browse Resources -> text-editor://session_id
# Full VS Code editor with multiline, syntax highlighting, etc.

# Retrieve edited content
content = await get_text_content(session_id="meeting_notes_abc123")
```

**How it works:**

1. Tool creates a resource: `text-editor://session_id`
2. User opens **Command Palette** → **"MCP: Browse Resources"**
3. Clicks on the resource to open in **VS Code editor**
4. Edits with **full multiline capabilities**
5. Saves and retrieves content

### 3. **Prompts** (Guided Workflows) ⭐ **NEW**

*Slash commands for structured interactions*

**Best for:** Multi-step processes, guided content creation  
**Usage:** `/mcp.human-in-the-loop-v4-dev.prompt_name`

```bash
# In VS Code chat:
/mcp.human-in-the-loop-v4-dev.multiline_text_workflow
/mcp.human-in-the-loop-v4-dev.guided_input_workflow
```

**Available Prompts:**

- `multiline_text_workflow` - Guided text creation with templates
- `guided_input_workflow` - Structured data input (JSON, YAML, code, etc.)

### 4. **Files** (Native File Editing) ⭐ **NEW**

*Temporary file creation for maximum VS Code integration*

**Best for:** Complex files, code editing, large documents  
**Tools:** `create_temp_file_editor`, `get_file_content`, `cleanup_temp_files`

```python
# Create temporary file
file_info = await create_temp_file_editor(
    purpose="Python script", 
    file_extension="py",
    initial_content="#!/usr/bin/env python3\n\n"
)

# User edits via: File -> Open -> /tmp/mcp_input_*.py
# Full VS Code with syntax highlighting, extensions, etc.

# Retrieve and cleanup
content = await get_file_content(file_id="abc123", cleanup=True)
```

## 🔄 Migration from v3.0

### ✅ **Backward Compatible**

All v3.0 tools still work exactly the same:

- `get_user_input` - Single-line input
- `get_user_choice` - Choice selection  
- `show_confirmation_dialog` - Confirmations
- `show_info_message` - Info messages
- `health_check` - Server status

### ⚠️ **Deprecated Tool**

- `get_multiline_input` - **DEPRECATED** (was single-line only due to MCP limitations)

### 🚀 **Recommended Upgrades**

| v3.0 Usage | v4.0 Replacement | Benefits |
|------------|------------------|----------|
| `get_multiline_input()` | `create_text_editor()` | True multiline editing in VS Code |
| Complex text input | `create_temp_file_editor()` | Native file editing with full features |
| Multi-step processes | Prompt workflows | Guided slash command interactions |

## 💡 Usage Examples

### Example 1: Simple Input (Unchanged)

```python
# Still works exactly the same as v3.0
name = await get_user_input(prompt="Enter your name")
color = await get_user_choice(prompt="Pick color", choices=["red", "blue"])
```

### Example 2: True Multiline Text ⭐ **NEW**

```python
# v3.0 (limited to single-line)
text = await get_multiline_input(prompt="Enter description")  # ❌ Single-line only

# v4.0 (true multiline editing)
editor = await create_text_editor(purpose="description", initial_text="")  # ✅ Full editor
# User edits in VS Code resource browser
content = await get_text_content(session_id="description_abc123")
```

### Example 3: Code Editing ⭐ **NEW**

```python
# Create Python file for editing
file_info = await create_temp_file_editor(
    purpose="data processor",
    file_extension="py", 
    initial_content="import pandas as pd\n\ndef process_data():\n    pass\n"
)

# User edits with full Python syntax highlighting, linting, etc.
# File -> Open -> /tmp/mcp_input_data_processor_*.py

# Retrieve final code
code = await get_file_content(file_id="abc123")
```

### Example 4: Guided Workflows ⭐ **NEW**

```bash
# In VS Code chat, use slash commands:
/mcp.human-in-the-loop-v4-dev.multiline_text_workflow purpose:"project proposal" example:"## Overview\nThis project will..." guidance:"Include timeline and budget sections"

# Creates guided workflow with template and instructions
```

## 🎯 When to Use Each Pattern

### 📝 **Simple Input → Elicitations**

- Single-line text fields
- Dropdown choices
- Yes/No confirmations  
- Quick info messages

### 📄 **Multiline Text → Resources**

- Meeting notes
- Documentation
- Email drafts
- Any multiline content

### 📁 **Complex Files → File System**

- Code files (.py, .js, .json, etc.)
- Configuration files
- Large documents
- Content needing syntax highlighting

### 🔄 **Guided Processes → Prompts**

- Multi-step data collection
- Template-based content creation
- Structured workflows
- Educational/tutorial interactions

## 🔍 Understanding MCP Limitations

### Why v3.0 Multiline Didn't Work
The MCP elicitation specification has fundamental constraints:
- Only supports primitive JSON Schema types: `string`, `number`, `boolean`, `enum`
- **No support** for `textarea`, `multiline`, `file upload`, or rich input types
- VS Code renders **all** string inputs as single-line Command Palette fields
- This is **by design** for security and consistency across MCP clients

### How v4.0 Solves This
Instead of fighting MCP limitations, v4.0 **leverages VS Code's strengths**:
- **Resources** → Native VS Code editor for multiline text
- **Files** → Native file system integration
- **Prompts** → Structured workflow guidance
- **Elicitations** → Simple inputs (what they're designed for)

## 🛠️ Tools Reference

### Legacy Tools (v3.0 compatible)
- `get_user_input` - Single-line text input
- `get_user_choice` - Multiple choice selection
- `show_confirmation_dialog` - Yes/No confirmations  
- `show_info_message` - Information display
- `health_check` - Server status
- `get_multiline_input` - **DEPRECATED** (use `create_text_editor`)

### New Resource Tools ⭐ 
- `create_text_editor` - Create editable text resource in VS Code
- `get_text_content` - Retrieve content from text editor session

### New File Tools ⭐
- `create_temp_file_editor` - Create temporary file for native editing
- `get_file_content` - Retrieve content from temporary file
- `cleanup_temp_files` - Clean up all temporary files

### New Information Tools ⭐
- `get_mcp_limitations_info` - Detailed explanation of MCP constraints

### New Prompt Workflows ⭐
- `/mcp.human-in-the-loop-v4-dev.multiline_text_workflow` - Guided text creation
- `/mcp.human-in-the-loop-v4-dev.guided_input_workflow` - Structured data input

### Available Resources ⭐
- `text-editor://{session_id}` - Editable text resources
- `user-content://{purpose}/{id}` - Parameterized content resources

## 📊 Performance & Cleanup

### Session Management
- Text sessions stored in memory during server runtime
- Automatic session ID generation
- Content persists until server restart

### File Management  
- Temporary files created in system temp directory
- Automatic cleanup on file retrieval (optional)
- Manual cleanup via `cleanup_temp_files` tool
- Cleanup on server shutdown

### Resource Management
- Resources are dynamic and created on-demand
- No persistent storage (content lives in memory)
- Session-based organization with UUIDs

## 🔧 Configuration

Update your `.vscode/mcp.json`:

```json
{
    "servers": {
        "human-in-the-loop-v4-dev": {
            "command": "uv",
            "args": ["run", "python", "human_loop_server_v4.py"],
            "cwd": "/path/to/mcp-server-Human-In-the-Loop-MCP-Server",
            "type": "stdio",
            "env": {
                "FASTMCP_LOG_LEVEL": "INFO",
                "MCP_REQUEST_TIMEOUT": "300",
                "MCP_CONNECTION_TIMEOUT": "30"
            }
        }
    }
}
```

## 🎉 Summary

**v4.0 Achievement:** Finally provides **true multiline input** that was impossible with MCP elicitations alone!

**Key Benefits:**
- ✅ **True multiline editing** via VS Code resources and files
- ✅ **Native VS Code integration** leveraging editor strengths  
- ✅ **Backward compatibility** with all v3.0 tools
- ✅ **Multiple interaction patterns** for optimal user experience
- ✅ **Comprehensive documentation** of MCP limitations and solutions
- ✅ **Guided workflows** via slash command prompts

**The Bottom Line:** v4.0 transforms the limitation of MCP elicitations into a feature by providing the **right tool for each type of user interaction**.
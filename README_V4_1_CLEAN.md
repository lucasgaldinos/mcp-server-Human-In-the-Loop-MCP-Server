# Human-in-the-Loop MCP Server v4.1 - Clean Implementation

A **simple, working** Model Context Protocol (MCP) server that provides 5 essential human interaction tools through VS Code's native Command Palette interface.

## What This Server Actually Does

✅ **5 Working Tools** that integrate seamlessly with VS Code:

1. **`get_user_input`** - Single-line text/number input via Command Palette
2. **`get_user_choice`** - Multiple choice selection with native picker
3. **`show_confirmation_dialog`** - Yes/No confirmations  
4. **`show_info_message`** - Information display with acknowledgment
5. **`health_check`** - Server status and capability information

## What This Server Does NOT Do

❌ **Multiline text editing** - MCP elicitations are inherently single-line only  
❌ **File editing** - No file system integration or text editors  
❌ **Rich UI components** - Limited to Command Palette interface  
❌ **External resources** - No resource creation or management  

## Why This Approach?

This server focuses on **what actually works** rather than complex "solutions" that don't function properly in practice. The MCP protocol has fundamental limitations that cannot be overcome through clever workarounds.

## Installation & Usage

### Prerequisites

- Python 3.11+ with `uv` package manager
- VS Code with MCP support
- FastMCP 2.12+

### Setup

1. **Install dependencies:**
   ```bash
   uv sync
   ```

2. **Configure VS Code MCP client** (`.vscode/mcp.json`):
   ```json
   {
     "servers": {
       "human-in-the-loop-clean": {
         "command": "uv",
         "args": ["run", "python", "human_loop_server_v4_1_clean.py"],
         "cwd": "/path/to/this/repository",
         "type": "stdio"
       }
     }
   }
   ```

3. **Restart VS Code** to load the MCP server

### Using the Tools

All tools appear in VS Code's Command Palette with native interfaces:

```python
# Example usage from an AI assistant:
await get_user_input(
    prompt="What's your project name?",
    title="Project Setup"
)

await get_user_choice(
    prompt="Select your preferred framework:",
    choices=["React", "Vue", "Angular", "Svelte"]
)

await show_confirmation_dialog(
    message="Delete all temporary files?",
    confirm_text="Delete",
    cancel_text="Keep"
)
```

## Architecture

### FastMCP 2.12 Compliance

- **Current API patterns**: Uses `ctx.elicit()` with proper Context injection
- **Type safety**: Pydantic Field definitions for all parameters
- **Error handling**: Comprehensive error handling and user feedback
- **Logging**: Detailed operation logging for debugging

### VS Code Integration

- **Command Palette**: All interactions use native VS Code Command Palette
- **No external UI**: No popup windows, browsers, or external applications
- **Lightweight**: Minimal resource usage and fast response times
- **Native feel**: Users interact through familiar VS Code interfaces

## Limitations & Alternatives

### MCP Protocol Limitations

The MCP protocol's elicitation system has fundamental constraints:

- **Single-line only**: All string inputs render as single-line Command Palette fields
- **No rich UI**: Cannot create textareas, file browsers, or complex forms
- **JSON schema limits**: Only supports primitive types (string, number, boolean, enum)

### For Multiline Text Input

If you need multiline text input, consider these alternatives:

1. **Direct file editing**: Have users create/edit files directly in VS Code
2. **External tools**: Use external applications designed for text input
3. **Copy/paste workflows**: Design workflows around clipboard operations
4. **Different protocols**: Consider non-MCP solutions for rich interactions

## Testing

```bash
# Run the server directly
uv run python human_loop_server_v4_1_clean.py

# Health check (once connected via VS Code MCP)
# Use Command Palette to test each tool
```

## API Reference

### get_user_input(prompt, title?, default_value?, input_type?)

Single-line text or number input via Command Palette.

**Parameters:**

- `prompt` (required): Question/prompt text
- `title`: Optional dialog title
- `default_value`: Optional pre-filled value
- `input_type`: "text", "integer", or "float"

**Returns:** User's input string or error message

### get_user_choice(prompt, choices, title?, allow_multiple?)

Multiple choice selection with native picker.

**Parameters:**

- `prompt` (required): Question/prompt text
- `choices` (required): Array of choice strings
- `title`: Optional dialog title
- `allow_multiple`: Always false (MCP limitation)

**Returns:** Selected choice string or error message

### show_confirmation_dialog(message, title?, confirm_text?, cancel_text?)

Yes/No confirmation dialog.

**Parameters:**

- `message` (required): Confirmation text
- `title`: Optional dialog title
- `confirm_text`: Custom confirm button text (default: "Yes")
- `cancel_text`: Custom cancel button text (default: "No")

**Returns:** Confirmation result or error message

### show_info_message(message, title?, info_type?)

Information display with acknowledgment.

**Parameters:**

- `message` (required): Information text
- `title`: Optional dialog title
- `info_type`: "info", "warning", "error", or "success"

**Returns:** Acknowledgment confirmation

### health_check()

Server status and capability information.

**Returns:** Comprehensive server health data including available tools, limitations, and environment info

## Version History

- **v4.1** - Clean implementation with 5 working tools only
- **v4.0** - Over-engineered with broken multiline solutions (removed)
- **v3.0** - Original working implementation
- **v2.x** - Earlier versions with different architectures

## Contributing

This project focuses on **simplicity and reliability**. When contributing:

1. Ensure all tools actually work in VS Code
2. Test with real users, not just theoretical scenarios
3. Prefer working simple solutions over complex broken ones
4. Document limitations honestly

## License

MIT License - See LICENSE file for details

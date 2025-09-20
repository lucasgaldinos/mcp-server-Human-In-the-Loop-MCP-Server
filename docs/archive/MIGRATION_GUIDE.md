# Migration Guide: v1.x to v2.0

This guide helps you migrate from Human-in-the-Loop MCP Server v1.x (GUI-based) to v2.0 (MCP prompt-based).

## 🔄 Overview of Changes

### What Changed

| Aspect | v1.x (GUI-based) | v2.0 (MCP Prompt-based) |
|--------|------------------|--------------------------|
| **User Interface** | tkinter GUI dialogs | MCP prompts in client |
| **Dependencies** | tkinter, platform-specific | FastMCP only |
| **Integration** | External GUI windows | Native MCP client integration |
| **Response Format** | Direct user data | Structured prompt metadata |
| **Platform Support** | GUI-dependent | Universal (any MCP client) |

### Why We Changed

1. **Better Integration**: MCP prompts integrate seamlessly with AI assistant workflows
2. **No GUI Dependencies**: Eliminates tkinter and platform-specific GUI issues
3. **Universal Compatibility**: Works with any MCP client, not just desktop environments
4. **Improved UX**: Users interact through their familiar MCP client interface
5. **Future-Proof**: Aligns with MCP ecosystem evolution

## 📋 Pre-Migration Checklist

- [ ] Backup your current v1.x configuration
- [ ] Identify all places where you use the MCP server
- [ ] Test your current workflows to understand expected behavior
- [ ] Ensure your MCP client supports prompts (VS Code with MCP extension does)
- [ ] Have Python 3.8+ available
- [ ] Install `uv` for dependency management (recommended)

## 🚀 Step-by-Step Migration

### Step 1: Install v2.0

```bash
# Navigate to your project directory
cd /path/to/mcp-server-Human-In-the-Loop-MCP-Server

# Pull latest changes (if using git)
git pull origin main

# Install v2.0 dependencies
uv sync

# Test the installation
uv run python test_manual.py
```

### Step 2: Update MCP Configuration

**Old v1.x Configuration (.vscode/mcp.json)**:
```json
{
    "servers": {
        "human-in-the-loop": {
            "command": "python",
            "args": ["human_loop_server.py"],
            "cwd": "/path/to/server"
        }
    }
}
```

**New v2.0 Configuration (.vscode/mcp.json)**:
```json
{
    "servers": {
        "human-in-the-loop-v2": {
            "command": "uv",
            "args": [
                "run", 
                "python", 
                "human_loop_server_v2.py"
            ],
            "cwd": "/path/to/mcp-server-Human-In-the-Loop-MCP-Server",
            "type": "stdio"
        }
    }
}
```

### Step 3: Update Your Integration Code

If you have custom code that interacts with the server, update it to handle the new response format.

**Old v1.x Response Format**:
```python
# v1.x returned direct user input
{
    "success": true,
    "result": "user's actual input here",
    "user_input": "user's actual input here"
}
```

**New v2.0 Response Format**:
```python
# v2.0 returns prompt metadata
{
    "success": true,
    "prompt_required": true,
    "prompt_name": "get_user_input_prompt",
    "prompt_params": {
        "title": "User Input",
        "prompt": "Enter your response:",
        "default_value": ""
    },
    "message": "User input requested: Enter your response:"
}
```

### Step 4: Test the Migration

```bash
# Test the new server
uv run python human_loop_server_v2.py --verify

# Run comprehensive tests
uv run python test_manual.py
```

### Step 5: Update Your Workflows

The new prompt-based system works differently:

1. **AI Assistant calls tool** (same as before)
2. **Server responds with prompt requirement** (new behavior)
3. **MCP client displays prompt** (new - handled by your MCP client)
4. **User responds through client** (new interface)
5. **Response flows back to AI** (continues workflow)

## 🔧 Common Migration Scenarios

### Scenario 1: Basic Text Input

**Before (v1.x)**:
```python
# AI assistant called tool and got direct response
result = await call_tool("get_user_input", {"prompt": "Enter name:"})
# result.user_input = "John Doe"
```

**After (v2.0)**:
```python
# AI assistant calls tool and gets prompt requirement
result = await call_tool("get_user_input", {"prompt": "Enter name:"})
# result.prompt_required = true
# MCP client handles the prompt automatically
# User's response flows back to AI assistant through MCP protocol
```

### Scenario 2: Multiple Choice Selection

**Before (v1.x)**:
```python
# Direct GUI dialog with immediate response
choices = ["Option A", "Option B", "Option C"]
result = await call_tool("get_user_choice", {"choices": choices})
# result.selected_choice = "Option B"
```

**After (v2.0)**:
```python
# Prompt-based selection through MCP client
choices = ["Option A", "Option B", "Option C"]
result = await call_tool("get_user_choice", {"choices": choices})
# result.prompt_required = true
# MCP client displays choice prompt
# User's selection flows back through MCP protocol
```

### Scenario 3: Confirmation Dialogs

**Before (v1.x)**:
```python
# Modal dialog blocking workflow
result = await call_tool("show_confirmation_dialog", {
    "message": "Delete file?"
})
# result.confirmed = true/false
```

**After (v2.0)**:
```python
# Non-blocking prompt through MCP client
result = await call_tool("show_confirmation_dialog", {
    "message": "Delete file?"
})
# result.prompt_required = true
# MCP client handles confirmation prompt
# User's decision flows back through MCP protocol
```

## 🐛 Troubleshooting Migration Issues

### Issue: "No GUI available" errors disappear

**Solution**: This is expected! v2.0 doesn't use GUI, so these errors won't occur.

### Issue: Different response format breaks existing code

**Solution**: Update your code to handle the new prompt-based responses:

```python
# Old code expecting direct results
if result.get("success") and result.get("user_input"):
    handle_user_input(result["user_input"])

# New code handling prompt requirements
if result.get("success") and result.get("prompt_required"):
    # MCP client will handle the prompt
    # Your AI assistant workflow continues when user responds
    pass
```

### Issue: MCP client doesn't show prompts

**Solution**: 
1. Verify your MCP client supports prompts
2. Check your `.vscode/mcp.json` configuration
3. Restart VS Code or your MCP client
4. Test with `uv run python test_manual.py`

### Issue: Server won't start

**Solution**:
```bash
# Check dependencies
uv sync

# Verify Python version
python --version  # Should be 3.8+

# Test server directly
uv run python human_loop_server_v2.py
```

## 📊 Feature Comparison

| Feature | v1.x Implementation | v2.0 Implementation | Migration Impact |
|---------|---------------------|---------------------|------------------|
| Text Input | tkinter.simpledialog | MCP input prompt | ✅ Seamless |
| Multiple Choice | tkinter radio buttons | MCP choice prompt | ✅ Enhanced |
| Confirmation | tkinter messagebox | MCP confirmation prompt | ✅ Improved |
| Info Messages | tkinter info dialog | MCP info prompt | ✅ Better integration |
| Error Handling | GUI error dialogs | MCP error responses | ✅ More robust |
| Cross-Platform | Platform-specific GUI | Universal MCP prompts | ✅ Better compatibility |

## 🎯 Benefits After Migration

### For Users
- **Consistent Interface**: All interactions through familiar MCP client
- **No GUI Dependencies**: Works in any environment (servers, containers, etc.)
- **Better Integration**: Seamless AI assistant workflows
- **Improved Reliability**: No GUI-related crashes or issues

### For Developers
- **Simpler Dependencies**: Just FastMCP, no GUI libraries
- **Better Testing**: Comprehensive test suite with 100% pass rate
- **Easier Deployment**: Works in headless environments
- **Future-Proof**: Aligned with MCP ecosystem evolution

### For System Administrators
- **Reduced Dependencies**: Fewer system requirements
- **Better Logging**: Enhanced logging and debugging
- **Easier Monitoring**: Built-in health checks
- **Container-Friendly**: Works in Docker and other containers

## 🔮 Post-Migration Validation

### Validation Checklist

- [ ] Server starts successfully: `uv run python human_loop_server_v2.py`
- [ ] All tests pass: `uv run python test_manual.py`
- [ ] MCP client recognizes the server
- [ ] Can see 6 tools and 5 prompts in MCP client
- [ ] AI assistant can trigger prompts successfully
- [ ] User can respond through MCP client interface
- [ ] Workflows complete end-to-end

### Performance Validation

```bash
# Run comprehensive tests
uv run python test_manual.py

# Expected output:
# 🏁 Testing Complete: 6/6 test suites passed
# 🎉 ALL TESTS PASSED! The Human-in-the-Loop MCP Server v2.0 is ready!
```

## 📞 Getting Help

### Support Resources

- **GitHub Issues**: Report bugs or ask questions
- **Documentation**: Check `docs/` directory for detailed guides
- **Test Suite**: Use `test_manual.py` to validate functionality
- **Migration Support**: Open an issue tagged with "migration"

### Common Questions

**Q: Can I run both v1.x and v2.0 simultaneously?**
A: Yes, use different server names in your MCP configuration.

**Q: Will my existing workflows break?**
A: The tool interface is the same, but response handling may need updates.

**Q: Can I revert to v1.x if needed?**
A: Yes, just switch back to the old configuration and server file.

**Q: Do I need to retrain users?**
A: No, users interact through their MCP client interface, which remains familiar.

---

**Need help with migration? Open an issue on GitHub or check our troubleshooting guide!**
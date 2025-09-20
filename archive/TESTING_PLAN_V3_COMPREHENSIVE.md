# MCP v3.0 Human-in-the-Loop Server - Comprehensive Testing Plan

## Overview

This testing plan validates all 6 tools in the Human-in-the-Loop MCP Server v3.0 that uses MCP elicitations for native VS Code dialogs.

## Testing Objectives

- ✅ Verify native VS Code Command Palette-style dialogs appear (not JSON responses)
- ✅ Validate all tool functionality and parameter handling
- ✅ Test error handling, timeouts, and cancellation scenarios
- ✅ Ensure server stability and crash prevention
- ✅ Document any issues and create improvement recommendations

## Tools Under Test

1. `mcp_human-in-the-_health_check` - Server status and capabilities
2. `mcp_human-in-the-_get_user_input` - Single-line text/number input
3. `mcp_human-in-the-_show_info_message` - Information display
4. `mcp_human-in-the-_show_confirmation_dialog` - Yes/No confirmations
5. `mcp_human-in-the-_get_user_choice` - Multiple choice selection
6. `mcp_human-in-the-_get_multiline_input` - Multi-line text input

## Testing Phases

### Phase 1: Basic Functionality Tests

**Objective:** Verify each tool works and produces native dialogs

#### Test 1.1: Health Check Verification

```
Tool: #mcp_human-in-the-_health_check
Expected: Server status, version 3.0.0, elicitation support = true
Priority: HIGH
```

#### Test 1.2: Basic Text Input

```
Tool: #mcp_human-in-the-_get_user_input
Parameters: {"prompt": "What's your name?", "input_type": "text"}
Expected: Native VS Code input dialog appears
Priority: HIGH
```

#### Test 1.3: Basic Info Message

```
Tool: #mcp_human-in-the-_show_info_message
Parameters: {"message": "Testing info display", "info_type": "info"}
Expected: Native VS Code info dialog with ℹ️ prefix
Priority: HIGH
```

#### Test 1.4: Basic Confirmation

```
Tool: #mcp_human-in-the-_show_confirmation_dialog
Parameters: {"message": "Do you want to continue?"}
Expected: Native VS Code Yes/No dialog
Priority: HIGH
```

#### Test 1.5: Basic Choice Selection

```
Tool: #mcp_human-in-the-_get_user_choice
Parameters: {"prompt": "Pick a color", "choices": ["Red", "Blue", "Green"]}
Expected: Native VS Code choice picker
Priority: HIGH
```

#### Test 1.6: Basic Multiline Input

```
Tool: #mcp_human-in-the-_get_multiline_input
Parameters: {"prompt": "Enter a description"}
Expected: Native VS Code multiline text input
Priority: HIGH
```

### Phase 2: Parameter Variation Tests

**Objective:** Test different parameter combinations and input types

#### Test 2.1: Integer Input Validation

```
Tool: #mcp_human-in-the-_get_user_input
Parameters: {"prompt": "Enter your age:", "input_type": "integer"}
Expected: Number validation in dialog
Priority: MEDIUM
```

#### Test 2.2: Float Input Validation

```
Tool: #mcp_human-in-the-_get_user_input
Parameters: {"prompt": "Enter height in meters:", "input_type": "float"}
Expected: Decimal number validation
Priority: MEDIUM
```

#### Test 2.3: Input with Title and Default

```
Tool: #mcp_human-in-the-_get_user_input
Parameters: {"title": "Contact Info", "prompt": "Email:", "default_value": "user@example.com"}
Expected: Dialog shows title and pre-filled value
Priority: MEDIUM
```

#### Test 2.4: All Info Message Types

```
Tool: #mcp_human-in-the-_show_info_message
Test each: info_type = "info", "warning", "error", "success"
Expected: Different emoji prefixes (ℹ️, ⚠️, ❌, ✅)
Priority: MEDIUM
```

#### Test 2.5: Custom Confirmation Buttons

```
Tool: #mcp_human-in-the-_show_confirmation_dialog
Parameters: {"message": "Save changes?", "confirm_text": "Save", "cancel_text": "Discard"}
Expected: Custom button text displayed
Priority: MEDIUM
```

#### Test 2.6: Long Choice List

```
Tool: #mcp_human-in-the-_get_user_choice
Parameters: {"prompt": "Select option", "choices": ["Option 1", "Option 2", ..., "Option 10"]}
Expected: Scrollable choice list
Priority: MEDIUM
```

### Phase 3: Error Handling Tests

**Objective:** Test cancellation, timeouts, and error scenarios

#### Test 3.1: User Cancellation Test

```
For each tool: User clicks Cancel/Escape
Expected: Graceful cancellation message, no server crash
Priority: HIGH
```

#### Test 3.2: Timeout Handling Test

```
For each tool: Wait for timeout period (if applicable)
Expected: Timeout message, server remains stable
Priority: HIGH
```

#### Test 3.3: Invalid Parameter Test

```
Tool: #mcp_human-in-the-_get_user_input
Parameters: {"input_type": "invalid_type"}
Expected: Graceful error handling
Priority: MEDIUM
```

#### Test 3.4: Empty Choice List Test

```
Tool: #mcp_human-in-the-_get_user_choice
Parameters: {"prompt": "Choose", "choices": []}
Expected: Error message or disabled state
Priority: MEDIUM
```

### Phase 4: Integration Tests

**Objective:** Test multiple tools in sequence

#### Test 4.1: Sequential Tool Calls

```
Sequence: health_check → get_user_input → show_info_message → show_confirmation_dialog
Expected: All tools work without interference
Priority: MEDIUM
```

#### Test 4.2: Rapid Fire Test

```
Call same tool multiple times quickly
Expected: Server handles concurrent requests gracefully
Priority: MEDIUM
```

### Phase 5: Performance and Stability Tests

**Objective:** Verify server stability and performance

#### Test 5.1: Server Restart Test

```
pkill -f human_loop_server_v3.py && restart
Expected: Clean restart, tools work immediately
Priority: HIGH
```

#### Test 5.2: Memory Leak Test

```
Call tools repeatedly over 10+ cycles
Expected: No memory leaks, stable performance
Priority: LOW
```

## Test Execution Guidelines

### Pre-Test Setup

1. Ensure VS Code Insiders is running with MCP support
2. Verify .vscode/mcp.json configuration is correct
3. Start human_loop_server_v3.py
4. Check server logs for successful startup

### During Testing

1. Test each tool using VS Code Chat with `#` prefix
2. Verify native dialogs appear (not JSON in chat)
3. Document exact behavior and any issues
4. Screenshot unusual behavior for later analysis

### Post-Test Analysis

1. Review server logs for errors
2. Check for any server crashes or hangs
3. Document performance observations
4. Create issue list and improvement recommendations

## Success Criteria

- ✅ All 6 tools produce native VS Code dialogs
- ✅ No JSON responses shown to users
- ✅ Graceful error handling for all scenarios
- ✅ Server remains stable throughout testing
- ✅ Response times under 2 seconds for basic operations

## Failure Scenarios to Watch For

- 🚫 JSON responses instead of native dialogs
- 🚫 Server crashes or hangs
- 🚫 Timeout errors without graceful handling
- 🚫 Dialog fails to appear
- 🚫 Error messages are confusing or technical

## Test Results Template

```
Tool: [tool_name]
Test: [test_description]
Status: PASS/FAIL/PARTIAL
Dialog Type: Native/JSON/None
Response Time: [seconds]
Issues: [description]
Notes: [additional observations]
```

## Next Steps After Testing

1. Update todo list with results
2. Create bug reports for any failures
3. Research solutions using web search tools
4. Implement fixes while keeping v3 version
5. Re-test after fixes
6. Document final status and recommendations

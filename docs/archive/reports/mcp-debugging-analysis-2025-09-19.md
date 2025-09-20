# Human-in-the-Loop MCP Server Research & Debugging Report

**Date:** September 19, 2025  
**Version:** 3.0 Analysis  
**Author:** AI Analysis Agent  

## Executive Summary

This report documents the investigation, debugging, and resolution of critical issues in the Human-in-the-Loop MCP Server v3.0, which provides native VS Code input dialogs through MCP elicitations. The analysis uncovered fundamental API mismatches that were causing incorrect behavior, particularly with choice selection returning indices instead of values.

## Problem Statement

### Initial Issues Identified

1. **Choice Selection Bug**: `get_user_choice` returned index (3) instead of actual choice value ("blue")
2. **Tool Similarity**: `get_multiline_input` and `get_user_input` appeared functionally identical
3. **Incomplete Testing**: `show_confirmation_dialog` had never been tested
4. **API Implementation Errors**: Incorrect use of MCP elicitation patterns

### User Feedback

- "The choices didn't appear. Though, the tools now kinda work."
- "My choice for `get_user_choice` was `3. blue`, not the index `{3}`."
- Tools were "kinda working" but not fully functional

## Research Methodology

### Phase 1: MCP Specification Research

**Sources Investigated:**

- <https://modelcontextprotocol.io/specification>
- <https://modelcontextprotocol.io/specification/2025-06-18/client/elicitation>
- <https://gofastmcp.com/servers/elicitation>
- DeepWiki for modelcontextprotocol/python-sdk

**Key Findings:**

1. **MCP Elicitation Protocol (2025-06-18)**:
   - Uses `elicitation/create` requests with JSON Schema
   - Supports flat objects with primitive properties only
   - Response actions: "accept", "decline", "cancel"
   - Schema types: string, number, boolean, enum

2. **FastMCP Implementation**:
   - Uses `ctx.elicit(message, response_type=...)` API
   - Supports scalar types (str, int, float)
   - Choice selection via list of strings: `["red", "green", "blue"]`
   - No response type: `response_type=None`

### Phase 2: Version & API Investigation

**Current Environment:**

- FastMCP Version: 2.12.3
- Import Patterns: Both `from fastmcp import FastMCP, Context` and `from mcp.server.fastmcp import FastMCP, Context` work
- Elicit Signature: `(self, message: str, response_type: type[T] | list[str] | None = None)`

## Root Cause Analysis

### Primary Issue: API Parameter Mismatch

**Incorrect Implementation:**

```python
result = await ctx.elicit(message, schema=ChoiceInput)  # WRONG
```

**Correct Implementation:**

```python
result = await ctx.elicit(message, response_type=["red", "green", "blue"])  # RIGHT
```

### Secondary Issues

1. **Choice Presentation**: Original code created text input with numbered choices, not native choice picker
2. **Result Handling**: Accessed `result.data.value` instead of `result.data`
3. **Schema Complexity**: Used unnecessary Pydantic models for simple scalar types

## Solution Implementation

### Core Fixes Applied

1. **Import Optimization**:
   ```python
   # Changed from
   from mcp.server.fastmcp import FastMCP, Context
   # To
   from fastmcp import FastMCP, Context
   ```

2. **API Parameter Correction**:
   ```python
   # Before: schema= parameter
   result = await ctx.elicit(message, schema=StringInput)
   
   # After: response_type= parameter  
   result = await ctx.elicit(message, response_type=str)
   ```

3. **Choice Selection Fix**:
   ```python
   # Before: Text input with numbered list
   choices_text = "\n".join([f"{i+1}. {choice}" for i, choice in enumerate(choices)])
   result = await ctx.elicit(full_message, schema=ChoiceInput)
   
   # After: Native choice picker
   result = await ctx.elicit(message, response_type=choices)
   ```

4. **Result Access Pattern**:
   ```python
   # Before: Pydantic model access
   return str(result.data.value)
   
   # After: Direct value access
   return str(result.data)
   ```

### Tool-Specific Implementations

| Tool | Response Type | Use Case |
|------|---------------|----------|
| `get_user_input` | `str`, `int`, `float` | Single-line typed input |
| `get_multiline_input` | `str` | Multi-line text input |
| `get_user_choice` | `["option1", "option2"]` | Selection from choices |
| `show_confirmation_dialog` | `["Yes", "No"]` | Binary confirmation |
| `show_info_message` | `None` | Information display |
| `health_check` | N/A | Server status |

## Testing Results

### Systematic Testing Protocol

Each tool was tested using the inline chat `#mcp_human-in-the-_` prefix:

| Tool | Test Input | Expected Result | Actual Result | Status |
|------|------------|-----------------|---------------|---------|
| `health_check` | N/A | Server status | ✅ Comprehensive status | ✅ PASS |
| `show_info_message` | Success message | User acknowledgment | ✅ "User acknowledged" | ✅ PASS |
| `get_user_input` | "yes, it is working" | Return text | ✅ Returns actual text | ✅ PASS |
| `get_multiline_input` | Multi-line text | Return text | ✅ Returns text (but single-line UI) | ⚠️ ISSUE |
| `get_user_choice` | Select "blue" | "blue" value | ✅ "User selected: blue" | ✅ PASS |
| `show_confirmation_dialog` | Confirm action | Confirmation | ✅ "User confirmed: ..." | ✅ PASS |

### Key Improvements

1. **Choice Selection Fixed**: Now returns actual choice value ("blue") instead of index (3)
2. **All Tools Functional**: Every tool creates native VS Code dialogs
3. **Proper Response Handling**: Correct action/data patterns implemented
4. **Native UI Integration**: Command Palette-style prompts working as intended

## Outstanding Issues

### 1. Multiline Input Limitation

**Issue**: Both `get_user_input` and `get_multiline_input` create single-line input fields.

**Research Findings**:

- FastMCP elicitations may not support true multiline input UI
- Both tools use `response_type=str` which creates identical interfaces
- User reported inability to use Shift+Enter for new lines

**Potential Solutions**:

1. Research if FastMCP supports multiline schemas
2. Use different prompt patterns to hint multiline intent
3. Consider alternative approaches or document limitation

### 2. Tool Differentiation

Current tools that need better differentiation:

- `get_user_input` vs `get_multiline_input` (functionally identical)
- Could consolidate or find technical solution for true multiline

## Lessons Learned

### Context Loss Prevention

1. **API Documentation Drift**: Online examples showed outdated patterns
2. **Version Compatibility**: Multiple API patterns exist across FastMCP versions
3. **Testing Importance**: Assumptions about functionality proved incorrect
4. **User Feedback Value**: User accurately identified real problems

### Best Practices Established

1. **Always verify API signatures** before implementation
2. **Test each tool systematically** with actual user interaction
3. **Use native library patterns** over custom implementations
4. **Document limitations transparently**

## References

### Primary Sources

- [MCP Specification 2025-06-18](https://modelcontextprotocol.io/specification/2025-06-18)
- [FastMCP Elicitation Guide](https://gofastmcp.com/servers/elicitation)
- [MCP Elicitation Specification](https://modelcontextprotocol.io/specification/2025-06-18/client/elicitation)

### Code Examples Referenced

- [FastMCP User Elicitation Examples](https://gofastmcp.com/servers/elicitation#constrained-options)
- [DeepWiki MCP Python SDK Analysis](https://deepwiki.com/modelcontextprotocol/python-sdk)

### Research Tools Used

- VS Code GitHub Copilot inline chat testing
- Terminal-based FastMCP version verification
- Live API signature inspection
- Systematic tool testing protocol

## Next Steps

1. **Investigate multiline input solutions**
2. **Complete documentation updates**
3. **Consider tool consolidation or enhancement**
4. **Implement comprehensive error handling**
5. **Create production deployment guide**

## Conclusion

The Human-in-the-Loop MCP Server v3.0 now provides fully functional native VS Code input dialogs through correct FastMCP elicitation implementation. The primary issues have been resolved:

- ✅ Choice selection returns values, not indices
- ✅ All tools create native VS Code dialogs
- ✅ Confirmation dialog tested and working
- ✅ Proper API patterns implemented

The server successfully transforms AI-user interaction from JSON responses to seamless, native VS Code Command Palette-style prompts, achieving the original project objective.

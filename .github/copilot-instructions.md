# GitHub Copilot Instructions for Human-In-the-Loop MCP Server

## Project Overview

This is a Human-In-the-Loop Model Context Protocol (MCP) Server that enables AI assistants to interact with users through GUI dialogs. The project currently uses tkinter for cross-platform GUI dialogs but should migrate toward VS Code-native integration patterns.

## Key Architecture Patterns

### Current Implementation

- **FastMCP framework** for MCP server implementation
- **Cross-platform tkinter GUI** with platform-specific optimizations
- **Threading** for non-blocking dialog operations
- **Tool-based architecture** with discrete functions for each interaction type

### Core Tools Available

- `get_user_input` - Single-line text/number input
- `get_user_choice` - Multiple choice selections  
- `get_multiline_input` - Long-form text input
- `show_confirmation_dialog` - Yes/no confirmations
- `show_info_message` - Information display
- `health_check` - Server status monitoring

## Development Priorities

### Primary Goal: VS Code Integration

The project should migrate from tkinter dialogs to VS Code-native patterns:

1. **Chat Participants** - Use VS Code Chat API for user interactions
2. **Language Model Tools** - Convert dialogs to VS Code tool confirmations
3. **MCP Integration** - Leverage VS Code's built-in MCP client capabilities

### Code Organization Principles

- Keep `human_loop_server.py` as the main entry point
- Platform detection should remain for backward compatibility
- Use type hints and comprehensive error handling
- Maintain async/await patterns throughout

## File Structure Guidelines

```
├── human_loop_server.py     # Main MCP server (keep existing)
├── pyproject.toml          # Package configuration
├── docs/                   # All documentation
│   ├── CONTEXT.md         # Architecture analysis
│   ├── tasks/             # Task breakdowns
│   └── ToT/               # Tree of Thought analyses  
├── .github/               # GitHub workflows and instructions
└── tests/                 # Future test suite
```

## Coding Standards

### Python Style

- Use **Black** formatter (line length: 88)
- Type hints on all function signatures
- Comprehensive docstrings following Google style
- Exception handling with specific error types

### MCP Server Patterns

- Use `@mcp.tool()` decorator for exposed functions
- Include `ctx: Context` parameter for logging
- Return structured dictionaries with `success`, `error`, and result fields
- Use `Field(description=...)` for parameter documentation

### VS Code Extension Patterns (Future)

- Use TypeScript for VS Code extension development
- Follow VS Code extension API patterns
- Implement proper activation events
- Use `vscode.ChatRequestHandler` for chat participants

## Key Dependencies to Understand

### Current Stack

- `fastmcp` - MCP server framework
- `tkinter` - GUI dialogs (to be replaced)
- `pydantic` - Data validation and type checking

### Target Stack (Migration)

- VS Code Extension APIs
- `@vscode/prompt-tsx` - Advanced prompt engineering
- TypeScript/JavaScript for extension development

## Common Patterns and Anti-Patterns

### ✅ Good Patterns

- Async/await for all tool functions
- Platform detection for cross-compatibility  
- Non-blocking GUI operations with threading
- Structured error responses
- Timeout protection (5-minute default)

### ❌ Anti-Patterns

- Blocking synchronous operations
- Hard-coded platform assumptions
- Missing error handling
- GUI operations on main thread
- Tight coupling between dialog types

## Integration Context

### MCP Protocol Understanding

- Tools are invoked by AI assistants based on context
- User confirmation should be built into tool design
- Rich metadata helps AI choose appropriate tools
- Platform compatibility is essential for adoption

### VS Code Ecosystem Knowledge

- Chat participants provide domain expertise
- Language model tools enable agent mode automation
- MCP servers can run locally or remotely
- VS Code APIs provide deep editor integration

## Testing Approach

### Current Testing Needs

- GUI dialog functionality across platforms
- MCP server tool invocation
- Error handling and timeout scenarios
- Platform-specific behavior validation

### Future Testing Strategy

- VS Code extension integration tests
- Chat participant interaction flows
- Language model tool confirmation workflows
- End-to-end user experience validation

## Documentation Standards

- Keep README.md as primary user documentation
- Use `docs/CONTEXT.md` for architectural decisions
- Create `docs/tasks/TASKS.md` for detailed task tracking
- Document migration strategy in separate files

## Performance Considerations

- GUI dialogs should render within 500ms
- Tool responses must complete within 5-minute timeout
- Memory usage should remain minimal for background operation
- Platform detection should be cached, not repeated

## Security and Error Handling

- Validate all user inputs before processing
- Graceful degradation when GUI unavailable
- Clear error messages for debugging
- Platform-appropriate error dialogs

## Migration Strategy Notes

When working on VS Code integration:

1. Maintain backward compatibility with existing MCP clients
2. Create VS Code extension in parallel to current implementation  
3. Use feature flags to enable VS Code-specific behaviors
4. Document migration path for users

Remember: The goal is transforming external GUI interruptions into seamless VS Code workflow integration.

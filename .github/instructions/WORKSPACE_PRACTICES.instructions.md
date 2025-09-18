# Workspace Practices and Development Guidelines

## Code Style and Formatting

### Python Standards

- **Formatter**: Use Black with line length 88
- **Import organization**: Use isort with Black compatibility
- **Type hints**: Required on all public functions and methods
- **Docstrings**: Google style for all public APIs
- **Variable naming**: `snake_case` for variables and functions, `PascalCase` for classes

### Example Function Pattern

```python
async def get_user_input(
    title: str,
    prompt: str,
    default_value: str = "",
    input_type: Literal["text", "integer", "float"] = "text",
    ctx: Context = None
) -> Dict[str, Any]:
    """
    Get input from user through GUI dialog.
    
    Args:
        title: Dialog window title
        prompt: Question/prompt to show user
        default_value: Pre-filled value in input field
        input_type: Expected data type for validation
        ctx: MCP context for logging
        
    Returns:
        Dictionary containing success status, user input, and metadata
        
    Raises:
        ValueError: If input_type is invalid
        RuntimeError: If GUI system unavailable
    """
```

## Architecture Patterns

### MCP Tool Design Pattern

All MCP tools should follow this consistent structure:

1. **Function Signature**: Use Annotated types with Field descriptions
2. **Input Validation**: Validate parameters early
3. **Context Logging**: Use ctx parameter for operation tracking
4. **Error Handling**: Return structured responses with success/error fields
5. **Platform Compatibility**: Handle cross-platform differences gracefully

### Error Response Pattern

```python
# Success response
{
    "success": True,
    "result": actual_result,
    "metadata": additional_info,
    "platform": CURRENT_PLATFORM
}

# Error response
{
    "success": False,
    "error": "Clear error message",
    "error_type": "ValidationError|RuntimeError|TimeoutError",
    "platform": CURRENT_PLATFORM
}
```

## Project Structure Conventions

### Directory Organization

```
├── human_loop_server.py    # Main entry point - keep monolithic for now
├── pyproject.toml         # Package configuration and dependencies
├── README.md             # User-facing documentation
├── TODO.md               # Development task list
├── docs/                 # All documentation
│   ├── CONTEXT.md       # Architecture and migration analysis
│   ├── tasks/           # Detailed task breakdowns
│   │   └── TASKS.md
│   └── ToT/             # Tree of Thought analyses
├── .github/             # GitHub-specific files
│   ├── copilot-instructions.md
│   └── workflows/       # CI/CD (future)
└── tests/               # Test suite (future)
    ├── unit/
    ├── integration/
    └── gui/
```

### File Naming Conventions

- **Python files**: `snake_case.py`
- **Documentation**: `UPPERCASE.md` for main docs, `lowercase.md` for details
- **Config files**: Follow tool conventions (`pyproject.toml`, `.gitignore`)

## Design Patterns and Principles

### Builder Pattern for Dialog Creation

Use builder pattern when complexity increases:

```python
class DialogBuilder:
    def __init__(self):
        self.title = ""
        self.prompt = ""
        self.options = {}
    
    def with_title(self, title: str) -> "DialogBuilder":
        self.title = title
        return self
    
    def with_prompt(self, prompt: str) -> "DialogBuilder":
        self.prompt = prompt
        return self
    
    def build(self) -> Dialog:
        return Dialog(self.title, self.prompt, self.options)
```

### Strategy Pattern for Platform-Specific Code

```python
class PlatformGUIStrategy(ABC):
    @abstractmethod
    def create_dialog(self, config: DialogConfig) -> Any:
        pass

class WindowsGUIStrategy(PlatformGUIStrategy):
    def create_dialog(self, config: DialogConfig) -> Any:
        # Windows-specific implementation
        pass

class MacOSGUIStrategy(PlatformGUIStrategy):
    def create_dialog(self, config: DialogConfig) -> Any:
        # macOS-specific implementation
        pass
```

### Factory Pattern for Dialog Types

```python
def create_dialog(dialog_type: str, **kwargs) -> BaseDialog:
    dialog_map = {
        "input": InputDialog,
        "choice": ChoiceDialog,
        "multiline": MultilineDialog,
        "confirmation": ConfirmationDialog,
        "info": InfoDialog
    }
    return dialog_map[dialog_type](**kwargs)
```

## Testing Guidelines

### Test Structure (Future Implementation)

```python
# tests/unit/test_dialogs.py
import pytest
from unittest.mock import Mock, patch

class TestGetUserInput:
    @pytest.mark.asyncio
    async def test_successful_input(self):
        # Arrange
        mock_ctx = Mock()
        
        # Act
        result = await get_user_input("Test", "Enter value:", ctx=mock_ctx)
        
        # Assert
        assert result["success"] is True
        mock_ctx.info.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_gui_unavailable(self):
        # Test graceful degradation when GUI not available
        pass
```

### Integration Test Patterns

- Mock tkinter dialogs for automated testing
- Test cross-platform compatibility scenarios
- Validate MCP protocol compliance
- Test timeout and cancellation scenarios

## VS Code Integration Patterns (Migration Target)

### Chat Participant Pattern

```typescript
const handler: vscode.ChatRequestHandler = async (
    request: vscode.ChatRequest,
    context: vscode.ChatContext,
    stream: vscode.ChatResponseStream,
    token: vscode.CancellationToken
) => {
    // Handle user interaction through chat
    if (request.command === 'input') {
        // Convert to chat-based input collection
    }
};
```

### Language Model Tool Pattern

```typescript
class HumanInputTool implements vscode.LanguageModelTool<InputParams> {
    async prepareInvocation(options: InvocationOptions) {
        return {
            invocationMessage: "Requesting user input...",
            confirmationMessages: {
                title: "User Input Required",
                message: `Get input: ${options.input.prompt}`
            }
        };
    }
    
    async invoke(options: InvocationOptions) {
        // Use VS Code's native input mechanisms
        const result = await vscode.window.showInputBox({
            prompt: options.input.prompt,
            value: options.input.defaultValue
        });
        
        return new vscode.LanguageModelToolResult([
            new vscode.LanguageModelTextPart(result || "")
        ]);
    }
}
```

## Documentation Standards

### README Structure

1. **Project Overview** - What it does and why
2. **Installation** - Quick start and detailed setup
3. **Usage Examples** - Common use cases with code
4. **API Reference** - Tool descriptions and parameters
5. **Contributing** - Development setup and guidelines
6. **License and Links** - Legal and reference information

### Code Documentation

- **Module docstrings**: Purpose, main classes/functions, usage examples
- **Function docstrings**: Args, Returns, Raises, Examples
- **Inline comments**: Only for complex logic, not obvious code
- **Type hints**: Complete type information for better IDE support

### Architectural Decision Records (ADRs)

Document major decisions in `docs/ADR/`:

```
# ADR-001: Choose FastMCP over Python MCP SDK

## Status
Accepted

## Context
Need to choose MCP framework for server implementation...

## Decision
Use FastMCP for its simplicity and async support...

## Consequences
+ Faster development
+ Better async handling
- Less control over protocol details
```

## Git Workflow and Branching

### Branch Naming

- `feature/description` - New functionality
- `fix/issue-description` - Bug fixes  
- `docs/update-description` - Documentation updates
- `refactor/component-name` - Code restructuring

### Commit Message Format

```
type(scope): description

Longer explanation if needed

Fixes #123
```

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

## Performance Guidelines

### Response Time Targets

- **Tool invocation**: < 100ms initial response
- **GUI dialog display**: < 500ms to show
- **User interaction**: No artificial delays
- **Timeout handling**: 5-minute maximum, configurable

### Memory Management

- **Minimize persistent state** - Tools should be stateless
- **Clean up resources** - Close dialogs and threads properly  
- **Cache platform detection** - Don't repeat expensive checks
- **Limit concurrent dialogs** - Prevent resource exhaustion

## Security Considerations

### Input Validation

```python
def validate_input(value: str, input_type: str) -> Any:
    """Validate and convert user input safely."""
    if input_type == "integer":
        try:
            return int(value)
        except ValueError:
            raise ValueError(f"Invalid integer: {value}")
    # Additional validation logic
```

### Error Information Disclosure

- **Log detailed errors** internally for debugging
- **Return sanitized errors** to users to prevent information leakage
- **Never expose system paths** or sensitive configuration
- **Validate file paths** if file operations are added

## Migration Readiness

### Backward Compatibility Strategy

1. **Feature flags** for VS Code-specific behavior
2. **Interface abstraction** to support multiple backends
3. **Configuration options** for deployment scenarios
4. **Deprecation warnings** for tkinter-based features

### Extension Development Preparation

- **TypeScript setup** with proper tooling
- **VS Code extension structure** following best practices
- **Package.json configuration** for extension metadata
- **Testing framework** for extension functionality

Remember: These practices should evolve as the project migrates toward VS Code integration while maintaining the core human-in-the-loop functionality.

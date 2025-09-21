# Production Examples: Human-in-the-Loop MCP Server v3.0

This document provides real-world examples of how to use the Human-in-the-Loop MCP Server v3.0 with **native VS Code dialogs** in production environments.

## 🎯 Core Capabilities

### Native VS Code Integration

The v3.0 server provides seamless user interaction through VS Code's Command Palette-style dialogs using MCP elicitations. All interactions appear as native VS Code prompts.

### Available Tools

| Tool | Purpose | Response Type | Example Use |
|------|---------|---------------|-------------|
| `get_user_input` | Single-line input | `str`, `int`, `float` | File names, numbers, short text |
| `get_user_choice` | Selection from options | `["option1", "option2"]` | Menu choices, configurations |
| `get_multiline_input` | Text input | `str` | Descriptions, comments, documentation |
| `show_confirmation_dialog` | Yes/No decisions | `["Yes", "No"]` | Deployment confirmations, deletions |
| `show_info_message` | Information display | `None` | Status updates, notifications |
| `health_check` | Server status | N/A | Monitoring, diagnostics |

## 🎯 Production Use Cases

### 1. Code Review and Deployment Workflow

**Scenario**: AI assistant analyzes code and gets human approval for production deployment.

```python
# In your AI application using MCP client
async def code_review_workflow():
    # Analyze code changes
    changes = analyze_code_changes("src/")
    
    # Show analysis results to user
    info_result = await mcp_client.call_tool("show_info_message", {
        "title": "Code Analysis Complete", 
        "message": f"Found {len(changes)} changes. Critical issues: {count_critical(changes)}",
        "info_type": "info"
    })
    
    # Get deployment confirmation
    deploy_result = await mcp_client.call_tool("show_confirmation_dialog", {
        "title": "Production Deployment",
        "message": "All tests passed. Deploy to production?",
        "confirm_text": "Deploy Now",
        "cancel_text": "Cancel"
    })
    
    # VS Code will show native confirmation dialog
    # User sees: "Production Deployment: All tests passed. Deploy to production?"
    # With buttons: [Deploy Now] [Cancel]
    
    if "User confirmed" in deploy_result.get("result", ""):
        return await execute_deployment()
    else:
        return "Deployment cancelled by user"
```

### 2. Interactive Content Creation

**Scenario**: AI generates content with human input for customization and approval.

```python
async def content_creation_workflow():
    # Get content topic from user  
    topic_result = await mcp_client.call_tool("get_user_input", {
        "prompt": "What topic should we write about?",
        "title": "Content Creation",
        "input_type": "text"
    })
    
    topic = extract_user_input(topic_result)
    
    # Get target audience
    audience_result = await mcp_client.call_tool("get_user_choice", {
        "prompt": "Who is your target audience?",
        "title": "Audience Selection",
        "choices": ["Technical Developers", "Business Users", "General Public", "Students"]
    })
    
    audience = extract_choice(audience_result)
    
    # Generate content with AI
    content = await generate_content(topic, audience)
    
    # Get approval for generated content
    approval_result = await mcp_client.call_tool("show_confirmation_dialog", {
        "title": "Content Approval",
        "message": f"Generated {len(content)} words on '{topic}' for {audience}. Publish?",
        "confirm_text": "Publish",
        "cancel_text": "Revise"
    })
    
    if "User confirmed" in approval_result.get("result", ""):
        return await publish_content(content)
    else:
        # Get revision notes
        revision_result = await mcp_client.call_tool("get_multiline_input", {
            "prompt": "What changes would you like to make?",
            "title": "Revision Notes",
            "placeholder": "Describe the changes needed..."
        })
        
        return await revise_content(content, extract_user_input(revision_result))
```

### 3. Data Analysis with User Guidance

**Scenario**: AI analyzes data but needs human input for interpretation and next steps.

```python
async def data_analysis_workflow(dataset_path):
    # Perform automated analysis
    analysis_results = await analyze_dataset(dataset_path)
    
    # Show analysis summary
    await mcp_client.call_tool("show_info_message", {
        "title": "Analysis Complete",
        "message": f"Dataset: {len(analysis_results)} rows processed. Key insights found.",
        "info_type": "success"
    })
    
    # Get user's focus area
    focus_result = await mcp_client.call_tool("get_user_choice", {
        "prompt": "Which aspect should we focus on?",
        "title": "Analysis Focus",
        "choices": [
            "Trends and Patterns", 
            "Anomaly Detection", 
            "Predictive Modeling", 
            "Custom Analysis"
        ]
    })
    
    focus = extract_choice(focus_result)
    
    if focus == "Custom Analysis":
        # Get custom analysis parameters
        custom_params = await mcp_client.call_tool("get_multiline_input", {
            "prompt": "Describe the specific analysis you need:",
            "title": "Custom Analysis Parameters",
            "placeholder": "E.g., correlation between variables X and Y, filtered by conditions..."
        })
        
        return await perform_custom_analysis(analysis_results, extract_user_input(custom_params))
    else:
        return await perform_standard_analysis(analysis_results, focus)
```

### 4. Configuration Management

**Scenario**: AI helps configure complex systems with user validation.

```python
async def system_configuration_workflow():
    # Get configuration type
    config_type = await mcp_client.call_tool("get_user_choice", {
        "prompt": "What would you like to configure?",
        "title": "System Configuration",
        "choices": ["Database Settings", "API Endpoints", "Security Policies", "Performance Tuning"]
    })
    
    config_selection = extract_choice(config_type)
    
    if config_selection == "Database Settings":
        # Get database connection details
        db_host = await mcp_client.call_tool("get_user_input", {
            "prompt": "Database host:",
            "title": "Database Configuration",
            "input_type": "text",
            "default_value": "localhost"
        })
        
        db_port = await mcp_client.call_tool("get_user_input", {
            "prompt": "Database port:",
            "title": "Database Configuration", 
            "input_type": "integer",
            "default_value": "5432"
        })
        
        # Validate configuration
        validation_result = await validate_db_config(
            extract_user_input(db_host),
            int(extract_user_input(db_port))
        )
        
        if validation_result["valid"]:
            # Confirm application
            apply_result = await mcp_client.call_tool("show_confirmation_dialog", {
                "title": "Apply Configuration",
                "message": f"Configuration validated. Apply to {config_selection}?",
                "confirm_text": "Apply",
                "cancel_text": "Cancel"
            })
            
            if "User confirmed" in apply_result.get("result", ""):
                return await apply_configuration(config_selection, validation_result["config"])
        else:
            await mcp_client.call_tool("show_info_message", {
                "title": "Configuration Error",
                "message": f"Validation failed: {validation_result['error']}",
                "info_type": "error"
            })
```

## 🛠️ Helper Functions

### Result Extraction Utilities

```python
def extract_user_input(tool_result):
    """Extract user input from MCP tool result"""
    result = tool_result.get("result", "")
    # Handle different response formats
    if isinstance(result, str):
        return result
    return str(result)

def extract_choice(choice_result):
    """Extract selected choice from choice tool result"""
    result = choice_result.get("result", "")
    if "User selected:" in result:
        return result.split("User selected: ")[1].strip()
    return result

def is_confirmed(confirmation_result):
    """Check if user confirmed an action"""
    result = confirmation_result.get("result", "")
    return "User confirmed:" in result

def is_cancelled(tool_result):
    """Check if user cancelled an action"""  
    result = tool_result.get("result", "")
    return "cancelled" in result.lower()
```

### Error Handling Patterns

```python
async def safe_user_interaction(tool_name, params, retries=3):
    """Safely call user interaction tools with retry logic"""
    for attempt in range(retries):
        try:
            result = await mcp_client.call_tool(tool_name, params)
            
            if is_cancelled(result):
                return {"cancelled": True, "result": result}
            
            return {"success": True, "result": result}
            
        except Exception as e:
            if attempt == retries - 1:
                # Final attempt failed
                await mcp_client.call_tool("show_info_message", {
                    "title": "Interaction Error",
                    "message": f"Failed to get user input: {str(e)}",
                    "info_type": "error"
                })
                return {"error": True, "message": str(e)}
            
            # Wait before retry
            await asyncio.sleep(1)
    
    return {"error": True, "message": "Max retries exceeded"}
```

## 🚀 VS Code Integration Examples

### Using in VS Code Chat

Users can interact with the server through VS Code chat using the `#mcp_human-in-the-_` prefix:

```
User: #mcp_human-in-the-_get_user_choice prompt="Choose deployment environment" choices=["Development", "Staging", "Production"] title="Deployment Target"
```

This will show a native VS Code choice picker with the three options.

### Expected User Experience

1. **Native Dialogs**: All prompts appear as VS Code Command Palette-style dialogs
2. **No External Windows**: Everything stays within VS Code
3. **Keyboard Navigation**: Full keyboard support like other VS Code prompts
4. **Consistent Styling**: Matches VS Code's native UI theme

### Tool Response Formats

All tools return structured responses:

```json
{
  "result": "User selected: Production"
}
```

```json  
{
  "result": "User confirmed: Deploy to production environment?"
}
```

```json
{
  "result": "User cancelled input request: Enter deployment notes"
}
```

## 📊 Performance Considerations

### Best Practices

1. **Batch Related Prompts**: Group related user inputs to minimize interruptions
2. **Provide Context**: Include clear titles and descriptions in all prompts
3. **Handle Cancellation**: Always check for user cancellation and provide graceful handling
4. **Timeout Management**: Set appropriate timeouts for user interactions
5. **Default Values**: Provide sensible defaults to speed up common workflows

### Common Patterns

```python
# Good: Batch related inputs
async def gather_deployment_info():
    # Get all deployment info in sequence
    environment = await get_environment_choice()
    notes = await get_deployment_notes()
    confirmation = await confirm_deployment(environment, notes)
    return {"environment": environment, "notes": notes, "confirmed": confirmation}

# Avoid: Scattered individual prompts throughout complex logic
```

## 🔍 Monitoring and Debugging

### Health Check Usage

```python
# Check server status before critical operations
health_result = await mcp_client.call_tool("health_check", {})
print(health_result)
# Returns comprehensive server status including available tools
```

### Logging User Interactions

```python
import logging

async def logged_user_interaction(tool_name, params):
    logging.info(f"Requesting user input: {tool_name} with {params}")
    result = await mcp_client.call_tool(tool_name, params)
    logging.info(f"User response: {result}")
    return result
```

## 📝 Testing Strategies

### Unit Testing User Interactions

```python
# Mock MCP responses for testing
class MockMCPClient:
    def __init__(self, responses):
        self.responses = responses
        self.call_count = 0
    
    async def call_tool(self, tool_name, params):
        response = self.responses[self.call_count]
        self.call_count += 1
        return response

# Test workflow with predefined responses
async def test_deployment_workflow():
    mock_responses = [
        {"result": "User selected: Production"},
        {"result": "User confirmed: Deploy to production?"}
    ]
    
    mock_client = MockMCPClient(mock_responses)
    result = await deployment_workflow(mock_client)
    assert result.success
```

### Integration Testing

Test the actual MCP server using the inline chat tools to ensure all functionality works as expected in real VS Code environment.

## 🎯 Migration from v2.x

If upgrading from previous versions:

1. **Remove tkinter dependencies** - v3.0 uses native VS Code dialogs
2. **Update tool calls** - Response formats have changed
3. **Test all interactions** - Verify native dialog behavior
4. **Update error handling** - New response patterns for cancellation/errors

The v3.0 server provides significantly improved user experience with native VS Code integration while maintaining all the functionality of previous versions.
    })

    # Get target audience
    audience_result = await call_tool("get_user_choice", {
        "title": "Target Audience",
        "prompt": "Who is the target audience?",
        "choices": [
            "Technical developers",
            "Business stakeholders", 
            "General users",
            "Marketing teams",
            "C-level executives"
        ]
    })
    
    # Get content length
    length_result = await call_tool("get_user_choice", {
        "title": "Content Length",
        "prompt": "How long should the content be?",
        "choices": [
            "Brief (1-2 paragraphs)",
            "Medium (3-5 paragraphs)",
            "Long (6+ paragraphs)",
            "Full article (1000+ words)"
        ]
    })
    
    # All prompts are handled by MCP client
    # AI assistant receives responses and continues workflow
    return await generate_content_with_requirements(
        topic_result, audience_result, length_result
    )

```

### 3. Data Processing Pipeline

**Scenario**: AI processes data but needs human validation for sensitive operations.

```python
# Data processing workflow
async def data_processing_workflow():
    # Analyze dataset
    dataset_info = analyze_dataset("customer_data.csv")
    
    # Show analysis to user
    await call_tool("show_info_message", {
        "title": "Dataset Analysis",
        "message": f"""Dataset contains:
        - {dataset_info['rows']} rows
        - {dataset_info['columns']} columns
        - {dataset_info['sensitive_fields']} sensitive fields detected
        - Estimated processing time: {dataset_info['processing_time']}""",
        "info_type": "info"
    })
    
    # Get processing confirmation
    if dataset_info['sensitive_fields'] > 0:
        confirmation = await call_tool("show_confirmation_dialog", {
            "title": "Process Sensitive Data?",
            "message": f"This dataset contains {dataset_info['sensitive_fields']} sensitive fields. Continue processing?",
            "confirm_text": "Process with Care",
            "cancel_text": "Review First"
        })
        
        # MCP client handles the sensitive data confirmation
        if confirmation.get("prompt_required"):
            return await handle_sensitive_data_processing()
    
    # Get output format preference
    format_result = await call_tool("get_user_choice", {
        "title": "Output Format",
        "prompt": "Choose output format:",
        "choices": ["CSV", "JSON", "Excel", "Database"]
    })
    
    return await process_data_with_format(dataset_info, format_result)
```

### 4. Project Setup Assistant

**Scenario**: AI helps set up new projects with user-customized configuration.

```python
# Project setup workflow
async def project_setup_workflow():
    # Get project name
    name_result = await call_tool("get_user_input", {
        "title": "New Project Setup",
        "prompt": "What should we name your project?",
        "default_value": "my-awesome-project"
    })
    
    # Get project type
    type_result = await call_tool("get_user_choice", {
        "title": "Project Type",
        "prompt": "What type of project are you creating?",
        "choices": [
            "Web Application (React/Next.js)",
            "API Server (FastAPI/Flask)",
            "Desktop App (Python/Electron)",
            "Mobile App (React Native)",
            "Data Science (Jupyter/Python)",
            "Machine Learning (PyTorch/TensorFlow)"
        ]
    })
    
    # Get additional requirements
    requirements_result = await call_tool("get_multiline_input", {
        "title": "Additional Requirements",
        "prompt": "Describe any specific requirements or features:",
        "placeholder": "- Database integration\n- Authentication system\n- Docker deployment\n- CI/CD pipeline"
    })
    
    # Show setup plan
    setup_plan = generate_setup_plan(name_result, type_result, requirements_result)
    await call_tool("show_info_message", {
        "title": "Project Setup Plan",
        "message": f"Ready to create project with:\n{setup_plan}",
        "info_type": "success"
    })
    
    # Final confirmation
    confirmation = await call_tool("show_confirmation_dialog", {
        "title": "Create Project?",
        "message": "Proceed with project creation?",
        "confirm_text": "Create Project",
        "cancel_text": "Modify Plan"
    })
    
    return await execute_project_setup(confirmation)
```

### 5. Deployment Management

**Scenario**: AI manages deployments but requires human oversight for production changes.

```python
# Deployment workflow
async def deployment_workflow():
    # Check deployment status
    status = check_deployment_status()
    
    # Show current status
    await call_tool("show_info_message", {
        "title": "Deployment Status",
        "message": f"""Current Environment Status:
        - Dev: {status['dev']}
        - Staging: {status['staging']}
        - Production: {status['production']}
        
        Pending Changes: {len(status['pending_changes'])}""",
        "info_type": "info"
    })
    
    # Get deployment target
    target_result = await call_tool("get_user_choice", {
        "title": "Deployment Target",
        "prompt": "Where would you like to deploy?",
        "choices": ["Development", "Staging", "Production"]
    })
    
    # Production requires extra confirmation
    if target_result.get("selected") == "Production":
        # Get deployment notes
        notes_result = await call_tool("get_multiline_input", {
            "title": "Deployment Notes",
            "prompt": "Add deployment notes (required for production):",
            "placeholder": "- Fixed critical bug #123\n- Added new feature X\n- Updated dependencies"
        })
        
        # Final production confirmation
        confirmation = await call_tool("show_confirmation_dialog", {
            "title": "Production Deployment",
            "message": "⚠️ This will deploy to PRODUCTION. Are you sure?",
            "confirm_text": "Deploy to Production",
            "cancel_text": "Cancel"
        })
        
        return await handle_production_deployment(notes_result, confirmation)
    
    return await handle_standard_deployment(target_result)
```

## 🔧 Integration Patterns

### Pattern 1: Validation Pipeline

```python
class ValidationPipeline:
    def __init__(self, mcp_client):
        self.client = mcp_client
    
    async def validate_with_human(self, data, validation_type):
        """Generic human validation pattern"""
        
        # Show data to user
        await self.client.call_tool("show_info_message", {
            "title": f"{validation_type} Validation",
            "message": f"Please review the following data:\n{data}",
            "info_type": "info"
        })
        
        # Get validation decision
        result = await self.client.call_tool("show_confirmation_dialog", {
            "title": "Approve Data?",
            "message": f"Do you approve this {validation_type.lower()}?",
            "confirm_text": "Approve",
            "cancel_text": "Reject"
        })
        
        return result
    
    async def get_correction_input(self, error_message):
        """Get human input for corrections"""
        return await self.client.call_tool("get_multiline_input", {
            "title": "Correction Required",
            "prompt": f"Please provide corrections:\n\nError: {error_message}",
            "placeholder": "Describe the corrections needed..."
        })
```

### Pattern 2: Progressive Disclosure

```python
class ProgressiveWorkflow:
    """Show information progressively based on user choices"""
    
    async def run_progressive_workflow(self):
        # Start with basic choice
        basic_choice = await self.get_basic_preference()
        
        if basic_choice == "advanced":
            # Show advanced options
            advanced_options = await self.get_advanced_options()
            return await self.process_advanced(advanced_options)
        else:
            # Simple path
            return await self.process_simple(basic_choice)
    
    async def get_basic_preference(self):
        result = await call_tool("get_user_choice", {
            "title": "Configuration Level",
            "prompt": "How would you like to configure this?",
            "choices": ["Quick Setup", "Custom Setup", "Advanced Options"]
        })
        return result
    
    async def get_advanced_options(self):
        # Only shown if user chose advanced
        return await call_tool("get_multiline_input", {
            "title": "Advanced Configuration",
            "prompt": "Enter advanced configuration options:",
            "placeholder": "key=value\nflag=true\npath=/custom/path"
        })
```

### Pattern 3: Error Recovery

```python
class ErrorRecoveryWorkflow:
    """Handle errors with human intervention"""
    
    async def process_with_recovery(self, operation):
        max_retries = 3
        attempt = 0
        
        while attempt < max_retries:
            try:
                return await operation()
            except Exception as error:
                attempt += 1
                
                # Show error to user
                await call_tool("show_info_message", {
                    "title": f"Error (Attempt {attempt}/{max_retries})",
                    "message": f"Operation failed: {str(error)}",
                    "info_type": "error"
                })
                
                if attempt < max_retries:
                    # Get user decision on retry
                    retry_choice = await call_tool("show_confirmation_dialog", {
                        "title": "Retry Operation?",
                        "message": "Would you like to retry this operation?",
                        "confirm_text": "Retry",
                        "cancel_text": "Cancel"
                    })
                    
                    if not retry_choice.get("confirmed", False):
                        break
                else:
                    # Final attempt failed - get manual intervention
                    manual_fix = await call_tool("get_multiline_input", {
                        "title": "Manual Intervention Required",
                        "prompt": "All automatic retries failed. Please provide manual resolution:",
                        "placeholder": "Describe manual steps taken or alternative approach..."
                    })
                    
                    return await self.handle_manual_resolution(manual_fix)
        
        raise Exception(f"Operation failed after {max_retries} attempts")
```

## 🚀 Production Deployment Examples

### Docker Integration

```dockerfile
# Dockerfile for MCP server
FROM python:3.11-slim

WORKDIR /app
COPY . .

# Install dependencies
RUN pip install uv
RUN uv sync

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD uv run python -c "from human_loop_server_v2 import health_check; health_check()"

# Run server
CMD ["uv", "run", "python", "human_loop_server_v2.py"]
```

### Kubernetes Deployment

```yaml
# k8s-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: human-loop-mcp-server
spec:
  replicas: 2
  selector:
    matchLabels:
      app: human-loop-mcp-server
  template:
    metadata:
      labels:
        app: human-loop-mcp-server
    spec:
      containers:
      - name: mcp-server
        image: human-loop-mcp-server:v2.0
        ports:
        - containerPort: 8000
        env:
        - name: HUMAN_LOOP_LOG_LEVEL
          value: "INFO"
        - name: HUMAN_LOOP_TIMEOUT
          value: "300"
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
```

### CI/CD Integration

```yaml
# .github/workflows/deploy.yml
name: Deploy MCP Server
on:
  push:
    branches: [main]

jobs:
  test-and-deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    
    - name: Setup Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: |
        pip install uv
        uv sync
    
    - name: Run tests
      run: uv run python test_manual.py
    
    - name: Deploy to staging
      if: success()
      run: |
        # Deploy to staging environment
        kubectl apply -f k8s-staging.yaml
    
    - name: Human approval required
      if: success()
      uses: actions/github-script@v6
      with:
        script: |
          // This would integrate with the MCP server
          // to get human approval for production deployment
          const approval = await mcpClient.callTool('show_confirmation_dialog', {
            title: 'Deploy to Production?',
            message: 'Staging deployment successful. Deploy to production?'
          });
          
          if (!approval.confirmed) {
            core.setFailed('Deployment cancelled by user');
          }
    
    - name: Deploy to production
      if: success()
      run: kubectl apply -f k8s-production.yaml
```

## 📊 Monitoring and Analytics

### Usage Analytics

```python
# analytics.py
import asyncio
from datetime import datetime
from collections import defaultdict

class MCPUsageAnalytics:
    def __init__(self):
        self.tool_usage = defaultdict(int)
        self.prompt_usage = defaultdict(int)
        self.response_times = []
    
    async def track_tool_usage(self, tool_name, start_time, end_time):
        self.tool_usage[tool_name] += 1
        response_time = (end_time - start_time).total_seconds()
        self.response_times.append(response_time)
    
    async def generate_usage_report(self):
        report = await call_tool("show_info_message", {
            "title": "MCP Usage Report",
            "message": f"""Usage Statistics:
            
            Most Used Tools:
            {self.format_tool_usage()}
            
            Average Response Time: {sum(self.response_times)/len(self.response_times):.2f}s
            Total Interactions: {sum(self.tool_usage.values())}""",
            "info_type": "info"
        })
        return report
    
    def format_tool_usage(self):
        sorted_tools = sorted(self.tool_usage.items(), key=lambda x: x[1], reverse=True)
        return "\n".join(f"- {tool}: {count} uses" for tool, count in sorted_tools[:5])
```

### Health Monitoring

```python
# monitoring.py
import asyncio
from datetime import datetime, timedelta

class MCPHealthMonitor:
    def __init__(self, mcp_client):
        self.client = mcp_client
        self.health_history = []
    
    async def periodic_health_check(self):
        """Run health checks every 5 minutes"""
        while True:
            try:
                health_result = await self.client.call_tool("health_check", {})
                self.health_history.append({
                    "timestamp": datetime.now(),
                    "status": health_result.get("status", "unknown"),
                    "details": health_result
                })
                
                # Alert if unhealthy
                if health_result.get("status") != "healthy":
                    await self.send_health_alert(health_result)
                
                # Cleanup old history (keep last 24 hours)
                cutoff = datetime.now() - timedelta(hours=24)
                self.health_history = [
                    h for h in self.health_history 
                    if h["timestamp"] > cutoff
                ]
                
                await asyncio.sleep(300)  # 5 minutes
                
            except Exception as e:
                await self.handle_health_check_error(e)
    
    async def send_health_alert(self, health_result):
        await call_tool("show_info_message", {
            "title": "⚠️ MCP Server Health Alert",
            "message": f"Server health check failed:\n{health_result}",
            "info_type": "warning"
        })
```

## 🔒 Security Best Practices

### Input Validation

```python
# security.py
import re
from typing import Dict, Any, Optional

class MCPSecurityValidator:
    def __init__(self):
        self.sensitive_patterns = [
            r'password\s*[:=]\s*\S+',
            r'api[_-]?key\s*[:=]\s*\S+',
            r'secret\s*[:=]\s*\S+',
            r'\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b',  # Credit card
        ]
    
    def validate_user_input(self, input_data: str) -> Dict[str, Any]:
        """Validate user input for security issues"""
        issues = []
        
        # Check for sensitive data
        for pattern in self.sensitive_patterns:
            if re.search(pattern, input_data, re.IGNORECASE):
                issues.append(f"Potential sensitive data detected: {pattern}")
        
        # Check for code injection
        dangerous_keywords = ['eval', 'exec', 'import os', 'subprocess']
        for keyword in dangerous_keywords:
            if keyword.lower() in input_data.lower():
                issues.append(f"Potentially dangerous keyword: {keyword}")
        
        return {
            "is_safe": len(issues) == 0,
            "issues": issues,
            "sanitized_input": self.sanitize_input(input_data) if issues else input_data
        }
    
    def sanitize_input(self, input_data: str) -> str:
        """Basic input sanitization"""
        # Remove potential script tags
        input_data = re.sub(r'<script.*?</script>', '', input_data, flags=re.IGNORECASE | re.DOTALL)
        # Remove potential SQL injection patterns
        input_data = re.sub(r'(union|select|insert|delete|drop|update)\s+', '', input_data, flags=re.IGNORECASE)
        return input_data
    
    async def secure_prompt_handler(self, tool_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Secure wrapper for MCP tool calls"""
        
        # Validate inputs
        for key, value in params.items():
            if isinstance(value, str):
                validation = self.validate_user_input(value)
                if not validation["is_safe"]:
                    # Ask user to confirm with security warning
                    confirmation = await call_tool("show_confirmation_dialog", {
                        "title": "⚠️ Security Warning",
                        "message": f"Security issues detected in {key}:\n" + 
                                 "\n".join(validation["issues"]) + 
                                 "\n\nProceed anyway?",
                        "confirm_text": "Proceed (Risk)",
                        "cancel_text": "Cancel"
                    })
                    
                    if not confirmation.get("confirmed", False):
                        return {"success": False, "error": "Operation cancelled due to security concerns"}
                    
                    # Use sanitized input if proceeding
                    params[key] = validation["sanitized_input"]
        
        # Proceed with secure call
        return await call_tool(tool_name, params)
```

---

**These examples demonstrate the power and flexibility of the Human-in-the-Loop MCP Server v2.0 in real production environments. Adapt them to your specific use cases and requirements.**

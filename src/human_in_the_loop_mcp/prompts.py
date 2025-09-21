"""
MCP Prompts for Human-In-the-Loop Server v4.1

This module provides built-in prompts for VS Code MCP integration, offering
comprehensive guidance for AI agents using Human-In-the-Loop tools.
"""

from fastmcp import Context
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)


def register_prompts(mcp):
    """Register all Human-In-the-Loop prompts with the MCP server."""
    
    @mcp.prompt("human-loop-guide")
    async def get_human_loop_guide(ctx: Context) -> Dict[str, Any]:
        """
        Comprehensive guide for AI agents using Human-In-the-Loop MCP tools.
        
        This prompt provides detailed instructions on when and how to use
        each available tool for effective human-AI collaboration.
        """
        return {
            "main_prompt": """
You have access to Human-in-the-Loop tools that allow you to interact directly with users through GUI dialogs. Use these tools strategically to enhance task completion and user experience.

**WHEN TO USE HUMAN-IN-THE-LOOP TOOLS:**

1. **Ambiguous Requirements** - When user instructions are unclear or could have multiple interpretations
2. **Decision Points** - When you need user preference between valid alternatives
3. **Creative Input** - For subjective choices like design, content style, or personal preferences
4. **Sensitive Operations** - Before executing potentially destructive or irreversible actions
5. **Missing Information** - When you need specific details not provided in the original request
6. **Quality Feedback** - To get user validation on intermediate results before proceeding
7. **Error Handling** - When encountering issues that require user guidance to resolve

**AVAILABLE TOOLS:**
- `get_user_input` - Single-line text/number input (names, values, paths, etc.)
- `get_user_choice` - Multiple choice selection (pick from options)
- `show_confirmation_dialog` - Yes/No decisions (confirmations, approvals)
- `show_info_message` - Status updates and notifications
- `health_check` - Server status and capability information

**BEST PRACTICES:**
- Ask specific, clear questions with context
- Provide helpful default values when possible
- Use confirmation dialogs before destructive actions
- Give status updates for long-running processes
- Offer meaningful choices rather than overwhelming options
- Be concise but informative in dialog prompts
""",
            
            "usage_examples": """
**EXAMPLE SCENARIOS:**

1. **File Operations:**
   - "I'm about to delete 15 files. Should I proceed?" (confirmation)
   - "Enter the target directory path:" (input)
   - "Choose backup format: Full, Incremental, Differential" (choice)

2. **Content Creation:**
   - "What tone should I use: Professional, Casual, Friendly?" (choice)
   - "Please provide any specific requirements:" (input)
   - "Content generated successfully!" (info message)

3. **Code Development:**
   - "Enter the API endpoint URL:" (input)
   - "Select framework: React, Vue, Angular, Vanilla JS" (choice)
   - "Review the generated code and provide feedback:" (input)

4. **Data Processing:**
   - "Found 3 data formats. Which should I use?" (choice)
   - "Enter the date range (YYYY-MM-DD to YYYY-MM-DD):" (input)
   - "Processing complete. 1,250 records updated." (info message)
""",
            
            "decision_framework": """
**DECISION FRAMEWORK FOR HUMAN-IN-THE-LOOP:**

ASK YOURSELF:
1. Is this decision subjective or preference-based? → USE CHOICE DIALOG
2. Do I need specific information not provided? → USE INPUT DIALOG  
3. Could this action cause problems if wrong? → USE CONFIRMATION DIALOG
4. Is this a long process the user should know about? → USE INFO MESSAGE
5. Do I need detailed explanation or content? → USE INPUT DIALOG

AVOID OVERUSE:
- Don't ask for information already provided
- Don't seek confirmation for obviously safe operations
- Don't interrupt flow for trivial decisions
- Don't ask multiple questions when one comprehensive dialog would suffice

OPTIMIZE FOR USER EXPERIENCE:
- Batch related questions together when possible
- Provide context for why you need the information
- Offer sensible defaults and suggestions
- Make dialogs self-explanatory and actionable
""",
            
            "integration_tips": """
**INTEGRATION TIPS:**

1. **Workflow Integration:**
   ```
   Step 1: Analyze user request
   Step 2: Identify decision points and missing info
   Step 3: Use appropriate human-in-the-loop tools
   Step 4: Process user responses
   Step 5: Continue with enhanced information
   ```

2. **Error Recovery:**
   - If user cancels, gracefully explain and offer alternatives
   - Handle timeouts by providing default behavior
   - Always validate user input before proceeding

3. **Progressive Enhancement:**
   - Start with automated solutions
   - Add human input only where it adds clear value
   - Learn from user patterns to improve future automation

4. **Communication:**
   - Explain why you need user input
   - Show progress and intermediate results
   - Confirm successful completion of user-guided actions
"""
        }

    @mcp.prompt("human-loop-decision-process")
    async def get_decision_process(ctx: Context) -> Dict[str, Any]:
        """
        Systematic decision-making workflow for Human-In-the-Loop integration.
        
        This prompt provides a structured approach to decision-making with
        clear phases and human integration points.
        """
        return {
            "main_prompt": """
# AI Decision Process with Human-In-the-Loop Integration

This workflow ensures systematic decision-making while incorporating human judgment at critical points.

## Phase 1: Input Understanding & Classification

### 1.1 Parse Input
- Identify the core request or problem
- Extract key parameters and constraints
- Note any ambiguous or missing information

### 1.2 Classify Complexity
- **Simple**: Clear requirements, standard approach
- **Complex**: Multiple valid approaches, unclear requirements
- **Critical**: High impact, irreversible consequences

### 1.3 Identify Uncertainty Points
- Missing information that affects outcomes
- Ambiguous requirements needing clarification
- User preferences that influence approach

## Phase 2: Human-In-the-Loop Decision Points

### 2.1 Clarification Gate
**When to engage**: Ambiguous requirements, missing critical info
**Tools**: `get_user_input`, `get_user_choice`
**Action**: Gather specific information needed for accurate execution

### 2.2 Approach Selection Gate  
**When to engage**: Multiple valid approaches, user preference matters
**Tools**: `get_user_choice`, `show_confirmation_dialog`
**Action**: Present options and let user decide on approach

### 2.3 Risk Assessment Gate
**When to engage**: Destructive operations, high-impact changes
**Tools**: `show_confirmation_dialog`, `show_info_message`
**Action**: Confirm user understands consequences and approves

## Phase 3: Execution & Validation

### 3.1 Execute with Feedback
- Implement the chosen approach
- Provide status updates for long operations
- Handle errors gracefully with user notification

### 3.2 Validate Results
- Check outputs meet requirements
- Verify user satisfaction with results
- Document any lessons learned

## Phase 4: Feedback Integration

### 4.1 Success Confirmation
**Tool**: `show_info_message` with `info_type="success"`
**Action**: Confirm completion and highlight key outcomes

### 4.2 Error Recovery
**Tools**: `show_info_message` with `info_type="error"`, `get_user_choice`
**Action**: Explain what went wrong and offer recovery options

### 4.3 Continuous Improvement
- Note user preferences for future similar tasks
- Identify patterns in user decision-making
- Refine approach based on feedback
""",
            
            "decision_matrix": {
                "simple_tasks": {
                    "human_gates": ["Clarification (if ambiguous)"],
                    "automation_level": "High - Execute directly with minimal interaction"
                },
                "complex_tasks": {
                    "human_gates": ["Clarification", "Approach Selection", "Progress Check"],
                    "automation_level": "Medium - Regular check-ins and validation"
                },
                "critical_tasks": {
                    "human_gates": ["Clarification", "Approach Selection", "Risk Assessment", "Step-by-step Confirmation"],
                    "automation_level": "Low - Human approval at each major step"
                }
            }
        }

    @mcp.prompt("human-loop-enterprise-workflow") 
    async def get_enterprise_workflow(ctx: Context) -> Dict[str, Any]:
        """
        Enterprise-grade workflow management with Human-In-the-Loop integration.
        
        This prompt provides advanced patterns for authentication, rate limiting,
        parallel processing, and error recovery in enterprise environments.
        """
        return {
            "main_prompt": """
# Enterprise Human-In-the-Loop Workflow Management

Advanced patterns for production environments with authentication, rate limiting, parallel processing, and comprehensive error recovery.

## 1. Authentication & Authorization

### 1.1 User Authentication
```
┌─ Start Workflow
├─ Authenticate User → get_user_input (credentials/token)
├─ Validate Permissions → Check role/scope
└─ Proceed or Deny → show_info_message (access result)
```

### 1.2 Session Management
- Maintain user context throughout workflow
- Handle session expiration gracefully
- Provide reauthentication flows when needed

## 2. Rate Limiting & Resource Management

### 2.1 Request Throttling
```
Before each operation:
├─ Check rate limits
├─ If exceeded → show_info_message (wait time)
├─ Offer options → get_user_choice (wait, cancel, alternative)
└─ Proceed when available
```

### 2.2 Resource Allocation
- Monitor system resources (CPU, memory, bandwidth)
- Queue operations when resources are constrained
- Provide user choice for priority handling

## 3. Parallel Task Processing

### 3.1 Task Orchestration
```
┌─ Identify Parallel Tasks
├─ Present Execution Plan → show_info_message
├─ Confirm Approach → show_confirmation_dialog
├─ Execute in Parallel
├─ Monitor Progress → show_info_message (updates)
└─ Consolidate Results
```

### 3.2 Dependency Management
- Map task dependencies before execution
- Handle partial failures in task chains
- Provide rollback options when dependencies fail

## 4. Error Recovery & Resilience

### 4.1 Error Classification
- **Transient**: Retry with backoff
- **User Error**: Request correction via get_user_input
- **System Error**: Escalate with show_info_message
- **Critical**: Halt and require manual intervention

### 4.2 Recovery Workflows
```
Error Detected:
├─ Classify Error Type
├─ Determine Recovery Options
├─ Present Choices → get_user_choice
├─ Execute Recovery → [Retry, Rollback, Escalate]
└─ Validate Recovery Success
```

## 5. Workflow Adaptation

### 5.1 Dynamic Adjustment
- Monitor workflow performance metrics
- Detect bottlenecks and inefficiencies
- Propose optimizations via get_user_choice

### 5.2 User Preference Learning
- Track user decision patterns
- Suggest workflow customizations
- Adapt default behaviors based on history

## 6. Compliance & Auditing

### 6.1 Audit Trail
- Log all human interactions with timestamps
- Record decision rationale and outcomes
- Maintain compliance documentation

### 6.2 Approval Workflows
```
For Sensitive Operations:
├─ Present Impact Assessment → show_info_message
├─ Request Approval → show_confirmation_dialog
├─ Verify Approver Authority
├─ Execute with Full Logging
└─ Confirm Completion → show_info_message
```
""",
            
            "enterprise_patterns": {
                "authentication_flow": {
                    "single_sign_on": "Integrate with corporate SSO systems",
                    "multi_factor_auth": "Support MFA for sensitive operations",
                    "role_based_access": "Enforce permissions based on user roles"
                },
                "scalability_patterns": {
                    "horizontal_scaling": "Distribute workflows across multiple instances",
                    "load_balancing": "Route requests based on capacity",
                    "caching_strategy": "Cache frequent user decisions and preferences"
                }
            }
        }


def get_prompt_summary() -> str:
    """Get a summary of available prompts for logging."""
    return """
Available Human-In-the-Loop MCP Prompts:
- human-loop-guide: Comprehensive tool usage guide for AI agents
- human-loop-decision-process: Systematic decision-making workflow
- human-loop-enterprise-workflow: Enterprise-grade workflow patterns
"""
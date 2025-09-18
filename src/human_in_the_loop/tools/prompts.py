"""
MCP prompts for human-in-the-loop guidance.

This module provides prompts that give LLMs comprehensive guidance
on when and how to use human-in-the-loop tools effectively.
"""

from typing import Dict
from fastmcp import FastMCP


def register_prompts(mcp: FastMCP):
    """Register all human-in-the-loop prompts with the MCP server."""
    
    @mcp.prompt()
    async def get_human_loop_prompt() -> Dict[str, str]:
        """
        Get prompting guidance for LLMs on when and how to use human-in-the-loop tools.
        
        This tool returns comprehensive guidance that helps LLMs understand when to pause
        and ask for human input, decisions, or feedback during task execution.
        """
        guidance = {
            "main_prompt": """
You have access to Human-in-the-Loop tools that allow you to interact directly with users through GUI dialogs. Use these tools strategically to enhance task completion and user experience.

**CRITICAL PRINCIPLE:** Only interrupt the user when human input adds genuine value that cannot be automated or inferred.

**WHEN TO USE HUMAN-IN-THE-LOOP TOOLS:**

1. **Ambiguous Requirements** - When user instructions are unclear or could have multiple interpretations
2. **Decision Points** - When you need user preference between valid alternatives
3. **Creative Input** - For subjective choices like design, content style, or personal preferences
4. **Sensitive Operations** - Before executing potentially destructive or irreversible actions
5. **Missing Critical Information** - When you need specific details not provided in the original request
6. **Quality Feedback** - To get user validation on intermediate results before proceeding
7. **Error Handling** - When encountering issues that require user guidance to resolve

**AVAILABLE TOOLS:**
- `get_user_input` - Single-line text/number input (names, values, paths, etc.)
- `get_user_choice` - Multiple choice selection (pick from options)
- `get_multiline_input` - Long-form text (descriptions, code, documents)
- `show_confirmation_dialog` - Yes/No decisions (confirmations, approvals)
- `show_info_message` - Status updates and notifications
- `health_check` - Server status monitoring

**BEST PRACTICES:**
- Ask specific, clear questions with context
- Provide helpful default values when possible
- Use confirmation dialogs before destructive actions
- Give status updates for long-running processes
- Offer meaningful choices rather than overwhelming options
- Be concise but informative in dialog prompts""",
            
            "tool_specific_guidance": """
**DETAILED TOOL USAGE GUIDE:**

## get_user_input
**WHEN TO USE:**
- Need a specific value: API keys, URLs, file paths, names, numbers
- Missing configuration values that can't be reasonably guessed
- User needs to provide credentials or personal information
- Require a specific format or validation (dates, emails, etc.)

**HOW TO USE:**
```python
# For text input
result = get_user_input(
    title="Configuration Required",
    prompt="Enter your OpenAI API key:",
    input_type="text",
    default_value=""  # Leave empty for sensitive data
)

# For numeric input  
result = get_user_input(
    title="Processing Parameters",
    prompt="Enter the maximum number of records to process:",
    input_type="integer", 
    default_value="1000"
)
```

**BEST PRACTICES:**
- Explain WHY you need the information
- Use appropriate input_type: "text", "integer", "float"
- Provide sensible defaults when safe to do so
- Validate the input before proceeding

---

## get_user_choice
**WHEN TO USE:**
- Multiple valid options exist and user preference matters
- Need to select from a predefined list of configurations
- User should choose between different approaches or strategies
- Selecting from available options (files, formats, methods)

**HOW TO USE:**
```python
# Single choice
result = get_user_choice(
    title="Framework Selection",
    prompt="Which web framework would you like to use?",
    choices=["React", "Vue.js", "Angular", "Svelte"],
    allow_multiple=False
)

# Multiple choices
result = get_user_choice(
    title="Features to Include", 
    prompt="Select which features to implement:",
    choices=["Authentication", "Database", "API", "Tests", "Docker"],
    allow_multiple=True
)
```

**BEST PRACTICES:**
- Limit choices to 2-8 options (avoid overwhelming)
- Order choices logically (most common first, alphabetical, etc.)
- Use clear, descriptive option names
- Consider allowing multiple selections when appropriate

---

## get_multiline_input
**WHEN TO USE:**
- Need detailed descriptions, requirements, or specifications
- User should provide code, templates, or long-form content
- Collecting feedback, reviews, or detailed explanations
- When single-line input would be insufficient

**HOW TO USE:**
```python
result = get_multiline_input(
    title="Project Requirements",
    prompt="Please describe your project requirements in detail:",
    default_value="Include:\n- Main features\n- Technical constraints\n- Timeline"
)

# For code input
result = get_multiline_input(
    title="Code Review",
    prompt="Paste the code you'd like me to review:",
    default_value=""
)
```

**BEST PRACTICES:**
- Provide helpful templates or examples in default_value
- Explain the expected format or structure
- Use for content that benefits from formatting/structure
- Give clear instructions about what information is needed

---

## show_confirmation_dialog
**WHEN TO USE:**
- Before destructive operations (delete, overwrite, reset)
- Before expensive operations (large downloads, long processes)
- When about to make irreversible changes
- Before proceeding with potentially risky actions

**HOW TO USE:**
```python
result = show_confirmation_dialog(
    title="Confirm Deletion",
    message="This will permanently delete 15 files. This action cannot be undone. Continue?"
)

# Check the result
if result.get("success") and result.get("result"):
    # User clicked "Yes"
    proceed_with_deletion()
else:
    # User clicked "No" or dialog failed
    abort_operation()
```

**BEST PRACTICES:**
- Clearly state what will happen and consequences
- Mention if the action is irreversible
- Include quantities/scope ("delete 15 files", "process 1000 records")
- Use when the risk/impact justifies the interruption

---

## show_info_message
**WHEN TO USE:**
- Notify about completion of long-running tasks
- Provide important status updates during complex processes
- Inform about successful operations with meaningful results
- Share important information the user should be aware of

**HOW TO USE:**
```python
# Process completion
show_info_message(
    title="Processing Complete",
    message="Successfully processed 1,250 records. 3 errors encountered and logged."
)

# Status update
show_info_message(
    title="Download Progress", 
    message="Large file download started. This may take 10-15 minutes. You can continue working."
)
```

**BEST PRACTICES:**
- Include specific, meaningful details (numbers, outcomes)
- Mention next steps if applicable
- Use for information that adds value, not just confirmations
- Include timing estimates for long processes

---

## health_check
**WHEN TO USE:**
- Diagnosing issues with the human-in-the-loop system
- Verifying GUI availability before showing dialogs
- Troubleshooting connection or platform problems
- Checking server status for debugging

**HOW TO USE:**
```python
health = health_check()
if health.get("gui_available"):
    # Can show GUI dialogs
    proceed_with_dialog()
else:
    # Fall back to text-based interaction
    use_alternative_approach()
```""",
            
            "decision_flowchart": """
**DECISION FLOWCHART: Which Tool Should I Use?**

START: Do I need human input?
├─ NO → Continue with automation
└─ YES → What type of input?
    ├─ SIMPLE VALUE (text/number) → get_user_input
    ├─ CHOICE FROM OPTIONS → get_user_choice  
    ├─ DETAILED TEXT/CODE → get_multiline_input
    ├─ YES/NO DECISION → show_confirmation_dialog
    ├─ STATUS/NOTIFICATION → show_info_message
    └─ SYSTEM STATUS → health_check

**COMPLEXITY GUIDELINES:**
- SIMPLE: Single value, clear question → get_user_input
- MODERATE: Multiple options, user preference → get_user_choice
- COMPLEX: Detailed requirements, long text → get_multiline_input
- CRITICAL: Confirm risky actions → show_confirmation_dialog
- INFORMATIONAL: Share results/status → show_info_message

**INTERRUPTION THRESHOLD:**
Only interrupt if the human input is:
✅ NECESSARY - Cannot proceed without it
✅ VALUABLE - Significantly improves the outcome  
✅ TIMELY - Better to ask now than later
✅ CLEAR - User can provide a meaningful response

❌ AVOID interrupting for:
- Information already provided
- Trivial preferences with obvious defaults
- Questions user can't reasonably answer
- Excessive confirmations for safe operations""",
            
            "usage_examples": """
**REAL-WORLD USAGE SCENARIOS:**

### 1. File Operations
```python
# GOOD: Before destructive action
confirm = show_confirmation_dialog(
    title="Confirm File Deletion",
    message="Delete 15 backup files older than 30 days? This cannot be undone."
)

# GOOD: Need specific path
target_dir = get_user_input(
    title="Backup Location", 
    prompt="Enter the backup directory path:",
    input_type="text",
    default_value="/home/user/backups"
)

# GOOD: Choose format
format_choice = get_user_choice(
    title="Backup Format",
    prompt="Select backup compression format:",
    choices=["ZIP", "TAR.GZ", "7Z"],
    allow_multiple=False
)
```

### 2. Content Creation
```python
# GOOD: Subjective style choice
tone = get_user_choice(
    title="Content Style",
    prompt="What tone should the blog post have?",
    choices=["Professional", "Casual", "Technical", "Friendly"],
    allow_multiple=False
)

# GOOD: Detailed requirements
requirements = get_multiline_input(
    title="Article Requirements",
    prompt="Describe the article requirements:",
    default_value="Topic:\nTarget audience:\nKey points to cover:\nWord count:"
)

# GOOD: Completion notification with details
show_info_message(
    title="Article Generated",
    message="Created 1,200-word article on 'AI Ethics'. Includes 5 sections, 3 citations, and SEO optimization."
)
```

### 3. Development Tasks
```python
# GOOD: Framework selection affects architecture
framework = get_user_choice(
    title="Project Framework",
    prompt="Choose the web framework for your project:",
    choices=["React + TypeScript", "Vue.js", "Angular", "Vanilla JS"],
    allow_multiple=False
)

# GOOD: API configuration
api_key = get_user_input(
    title="API Configuration",
    prompt="Enter your API key for the external service:",
    input_type="text"
)

# GOOD: Code review feedback
feedback = get_multiline_input(
    title="Code Review",
    prompt="Review this code and provide feedback:",
    default_value="Strengths:\n\nImprovements:\n\nSecurity concerns:"
)
```

### 4. Data Processing
```python
# GOOD: Format selection when multiple valid options
data_format = get_user_choice(
    title="Data Export Format",
    prompt="Which format should I use for the data export?",
    choices=["CSV", "JSON", "Excel", "XML"],
    allow_multiple=False
)

# GOOD: Processing parameters
batch_size = get_user_input(
    title="Processing Configuration",
    prompt="Enter batch size for processing (1-10000):",
    input_type="integer",
    default_value="1000"
)

# GOOD: Processing complete with statistics  
show_info_message(
    title="Data Processing Complete",
    message="Processed 15,847 records in 3.2 minutes. 12 duplicates removed, 3 errors logged."
)
```

### 5. Error Handling
```python
# GOOD: When user input needed to resolve error
recovery_action = get_user_choice(
    title="Connection Error",
    prompt="Failed to connect to database. How should I proceed?",
    choices=["Retry with same settings", "Use backup database", "Skip database operations", "Cancel task"],
    allow_multiple=False
)

# GOOD: Get alternative when original fails
alternative_path = get_user_input(
    title="File Not Found",
    prompt="Original file not found. Enter alternative file path:",
    input_type="text"
)
```""",
            
            "integration_tips": """
**ADVANCED INTEGRATION STRATEGIES:**

### 1. Workflow Integration
```python
# Step 1: Analyze user request
user_intent = analyze_request(user_input)

# Step 2: Identify decision points and missing info
missing_info = identify_gaps(user_intent)

# Step 3: Use appropriate human-in-the-loop tools
if missing_info.requires_choice:
    choice = get_user_choice(...)
elif missing_info.needs_details:
    details = get_multiline_input(...)
elif missing_info.needs_value:
    value = get_user_input(...)

# Step 4: Process user responses and continue
enhanced_request = merge_user_input(user_intent, user_responses)
execute_with_confirmation(enhanced_request)
```

### 2. Error Recovery Patterns
```python
try:
    result = execute_operation()
except ConfigurationError as e:
    # Get missing configuration
    config_value = get_user_input(
        title="Configuration Required",
        prompt=f"Missing {e.parameter}. Please provide:",
        input_type=e.expected_type
    )
    retry_with_config(config_value)
    
except AmbiguousInputError as e:
    # Clarify user intent
    clarification = get_user_choice(
        title="Clarification Needed",
        prompt=f"Did you mean:",
        choices=e.possible_interpretations
    )
    retry_with_clarification(clarification)
```

### 3. Progressive Enhancement
```python
# Start with automation
automated_result = attempt_automated_solution()

if automated_result.confidence < 0.8:
    # Add human validation for low-confidence results
    confirmation = show_confirmation_dialog(
        title="Verify Result",
        message=f"I generated: {automated_result.output}. Is this correct?"
    )
    
    if not confirmation["result"]:
        # Get user correction
        correction = get_multiline_input(
            title="Provide Correction",
            prompt="Please provide the correct version:",
            default_value=automated_result.output
        )
        final_result = apply_correction(correction)
```

### 4. User Experience Optimization
```python
# Batch related questions
user_prefs = collect_user_preferences([
    ("Framework", ["React", "Vue", "Angular"]),
    ("Styling", ["CSS", "SCSS", "Tailwind"]), 
    ("Testing", ["Jest", "Vitest", "Cypress"])
])

# Provide context for why input is needed
api_key = get_user_input(
    title="API Integration Setup",
    prompt="To enable real-time data sync, please enter your API key. This will be stored securely.",
    input_type="text"
)

# Show progress for long operations
show_info_message(
    title="Processing Started",
    message="Analyzing 50,000 records. Estimated time: 5-7 minutes. I'll notify you when complete."
)

# Follow up with results
show_info_message(
    title="Analysis Complete", 
    message="Found 1,247 anomalies, 15 critical issues. Full report saved to analysis_report.pdf"
)
```"""
        }
        
        return guidance
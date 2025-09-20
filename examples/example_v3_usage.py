#!/usr/bin/env python3
"""
Example Usage: Human-in-the-Loop MCP Server v3.0

This example demonstrates how the new elicitation-based server creates
native VS Code input dialogs instead of complex JSON responses.

When you use these tools in VS Code with MCP:
1. Call a tool like get_user_input
2. VS Code shows a Command Palette-style input dialog  
3. User types their response directly in VS Code
4. No complex JSON - just clean, native user interface!
"""

def example_usage():
    """Examples of how the v3.0 server works with native VS Code dialogs"""
    
    print("🚀 HUMAN-IN-THE-LOOP MCP SERVER v3.0 - USAGE EXAMPLES")
    print("=" * 60)
    
    print("\n💡 NEW IN v3.0: NATIVE VS CODE DIALOGS!")
    print("Instead of complex JSON responses, you get:")
    print("  ✨ Command Palette-style input fields")
    print("  ✨ Native VS Code choice pickers") 
    print("  ✨ Clean confirmation dialogs")
    print("  ✨ Simple information messages")
    
    print("\n📋 AVAILABLE TOOLS:")
    
    tools = [
        {
            "name": "get_user_input",
            "description": "Single-line text input - creates VS Code input field",
            "example": "Ask user for their name, email, or any text"
        },
        {
            "name": "get_user_choice", 
            "description": "Multiple choice selection - creates VS Code choice picker",
            "example": "Let user choose from options like 'Small', 'Medium', 'Large'"
        },
        {
            "name": "get_multiline_input",
            "description": "Multi-line text input - creates VS Code text area", 
            "example": "Ask user for descriptions, code, or longer content"
        },
        {
            "name": "show_confirmation_dialog",
            "description": "Yes/No confirmation - creates VS Code confirmation dialog",
            "example": "Ask 'Are you sure you want to delete this file?'"
        },
        {
            "name": "show_info_message",
            "description": "Information display - creates VS Code info dialog",
            "example": "Show status messages, warnings, or success notifications"
        },
        {
            "name": "health_check",
            "description": "Server status check - shows capabilities and health info",
            "example": "Verify server is working and see available features"
        }
    ]
    
    for i, tool in enumerate(tools, 1):
        print(f"\n{i}. {tool['name']}")
        print(f"   📝 {tool['description']}")
        print(f"   💡 Example: {tool['example']}")
    
    print("\n🎯 THE KEY DIFFERENCE:")
    print("  OLD v2.0: Returns complex JSON like:")
    print('    {"success": true, "prompt_required": true, "prompt_type": "get_user_input_prompt"...}')
    print("  NEW v3.0: Shows native VS Code dialog and returns simple result:")
    print('    "User entered: John Smith"')
    
    print("\n🔧 HOW TO USE:")
    print("1. Start the server: python human_loop_server_v3.py")
    print("2. Connect from VS Code MCP client")
    print("3. Call any tool - see native VS Code dialogs!")
    print("4. Enjoy clean, simple user interface!")
    
    print("\n✨ POWERED BY MCP ELICITATIONS")
    print("Uses ctx.elicit() to create native Command Palette-style prompts")

if __name__ == "__main__":
    example_usage()
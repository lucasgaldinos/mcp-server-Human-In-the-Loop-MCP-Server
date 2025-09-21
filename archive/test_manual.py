#!/usr/bin/env python3
"""
Manual testing script for the Human-in-the-Loop MCP Server v2.0

This script tests the functionality without requiring pytest framework.
"""

import asyncio
import sys
from pathlib import Path

# Add src to path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from fastmcp import FastMCP, Client
from human_in_the_loop.prompts import register_prompts
from human_in_the_loop.tools import register_tools
from human_in_the_loop.utils.helpers import validate_prompt_response, get_server_status


def test_response_validation():
    """Test response validation functionality."""
    print("🧪 Testing Response Validation...")
    
    test_cases = [
        ("Hello World", "text", True, "Hello World"),
        ("42", "integer", True, 42),
        ("3.14", "float", True, 3.14),
        ("yes", "confirmation", True, True),
        ("no", "confirmation", True, False),
        ("2", "choice", True, 2),
        ("1, 3, 5", "choice", True, [1, 3, 5]),
        ("", "text", False, None),
        ("not_a_number", "integer", False, None),
        ("maybe", "confirmation", False, None),
    ]
    
    passed = 0
    total = len(test_cases)
    
    for i, (response, response_type, expected_valid, expected_value) in enumerate(test_cases):
        try:
            valid, value, error = validate_prompt_response(response, response_type)
            
            if valid == expected_valid and (not expected_valid or value == expected_value):
                print(f"  ✅ Test {i+1}: {response_type} '{response}' -> {valid}, {value}")
                passed += 1
            else:
                print(f"  ❌ Test {i+1}: {response_type} '{response}' -> Expected {expected_valid}, {expected_value}, got {valid}, {value}")
        except Exception as e:
            print(f"  💥 Test {i+1}: {response_type} '{response}' -> Exception: {e}")
    
    print(f"🧪 Response Validation: {passed}/{total} tests passed\n")
    return passed == total


async def test_mcp_server_creation():
    """Test MCP server creation and registration."""
    print("🏗️ Testing MCP Server Creation...")
    
    try:
        # Create server
        mcp = FastMCP("Test Human-in-the-Loop Server")
        print("  ✅ Server created successfully")
        
        # Register prompts
        register_prompts(mcp)
        print("  ✅ Prompts registered successfully")
        
        # Register tools
        register_tools(mcp)
        print("  ✅ Tools registered successfully")
        
        # Check if prompts are registered
        prompt_count = len(mcp._prompt_manager._prompts)
        print(f"  ✅ {prompt_count} prompts registered")
        
        # Check if tools are registered
        tool_count = len(mcp._tool_manager._tools)
        print(f"  ✅ {tool_count} tools registered")
        
        print("🏗️ MCP Server Creation: SUCCESS\n")
        return True
        
    except Exception as e:
        print(f"  ❌ Server creation failed: {e}")
        print("🏗️ MCP Server Creation: FAILED\n")
        return False


async def test_tool_functionality():
    """Test all MCP tools using Client."""
    print("🔧 Testing Tool Functionality...")
    
    try:
        # Create server
        mcp = FastMCP("Tool Test Server")
        register_prompts(mcp)
        register_tools(mcp)
        
        # Test with Client
        async with Client(mcp) as client:
            # Get tools
            tools = await client.list_tools()
            print(f"  ✅ Listed {len(tools)} tools")
            
            # Test get_user_input
            result = await client.call_tool("get_user_input", {
                "title": "Test Input",
                "prompt": "Enter test data:",
                "default_value": "test"
            })
            if not result.is_error and result.data.get("success"):
                print("    ✅ get_user_input tool works")
            else:
                print(f"    ❌ get_user_input failed: {result.data}")
                return False
            
            # Test get_user_choice
            result = await client.call_tool("get_user_choice", {
                "title": "Test Choice",
                "prompt": "Choose an option:",
                "choices": ["Option 1", "Option 2", "Option 3"]
            })
            if not result.is_error and result.data.get("success"):
                print("    ✅ get_user_choice tool works")
            else:
                print(f"    ❌ get_user_choice failed: {result.data}")
                return False
            
            # Test get_multiline_input
            result = await client.call_tool("get_multiline_input", {
                "title": "Test Multiline",
                "prompt": "Enter multiple lines:",
                "placeholder": "Line 1\nLine 2"
            })
            if not result.is_error and result.data.get("success"):
                print("    ✅ get_multiline_input tool works")
            else:
                print(f"    ❌ get_multiline_input failed: {result.data}")
                return False
            
            # Test show_confirmation_dialog
            result = await client.call_tool("show_confirmation_dialog", {
                "title": "Test Confirmation",
                "message": "Do you confirm this action?",
                "confirm_text": "Yes",
                "cancel_text": "No"
            })
            if not result.is_error and result.data.get("success"):
                print("    ✅ show_confirmation_dialog tool works")
            else:
                print(f"    ❌ show_confirmation_dialog failed: {result.data}")
                return False
            
            # Test show_info_message
            result = await client.call_tool("show_info_message", {
                "title": "Test Info",
                "message": "This is a test message",
                "info_type": "info"
            })
            if not result.is_error and result.data.get("success"):
                print("    ✅ show_info_message tool works")
            else:
                print(f"    ❌ show_info_message failed: {result.data}")
                return False
            
            # Test health_check
            result = await client.call_tool("health_check", {})
            if not result.is_error and result.data.get("success"):
                print("    ✅ health_check tool works")
            else:
                print(f"    ❌ health_check failed: {result.data}")
                return False
        
        print("🔧 Tool Functionality: SUCCESS\n")
        return True
        
    except Exception as e:
        print(f"  ❌ Tool testing failed: {e}")
        print("🔧 Tool Functionality: FAILED\n")
        return False


async def test_prompt_functionality():
    """Test all MCP prompts using Client."""
    print("💬 Testing Prompt Functionality...")
    
    try:
        # Create server
        mcp = FastMCP("Prompt Test Server")
        register_prompts(mcp)
        register_tools(mcp)
        
        # Test with Client
        async with Client(mcp) as client:
            # Get prompts
            prompts = await client.list_prompts()
            print(f"  ✅ Listed {len(prompts)} prompts")
            
            # Test each prompt
            prompt_tests = [
                ("get_user_input_prompt", {
                    "title": "Test Input",
                    "prompt": "Enter test data:",
                    "default_value": "test"
                }),
                ("get_user_choice_prompt", {
                    "title": "Test Choice",
                    "prompt": "Choose an option:",
                    "choices": ["Option 1", "Option 2", "Option 3"]
                }),
                ("get_multiline_input_prompt", {
                    "title": "Test Multiline",
                    "prompt": "Enter multiple lines:",
                    "placeholder": "Line 1\nLine 2"
                }),
                ("show_confirmation_prompt", {
                    "title": "Test Confirmation",
                    "message": "Do you confirm this action?",
                    "confirm_text": "Yes",
                    "cancel_text": "No"
                }),
                ("show_info_message_prompt", {
                    "title": "Test Info",
                    "message": "This is a test message",
                    "info_type": "info"
                })
            ]
            
            for prompt_name, params in prompt_tests:
                try:
                    result = await client.get_prompt(prompt_name, params)
                    if result and hasattr(result, 'messages') and result.messages:
                        print(f"    ✅ {prompt_name} renders correctly")
                    else:
                        print(f"    ❌ {prompt_name} failed to render")
                        return False
                except Exception as e:
                    print(f"    ❌ {prompt_name} error: {e}")
                    return False
        
        print("💬 Prompt Functionality: SUCCESS\n")
        return True
        
    except Exception as e:
        print(f"  ❌ Prompt testing failed: {e}")
        print("💬 Prompt Functionality: FAILED\n")
        return False


def test_server_status():
    """Test server status functionality."""
    print("📊 Testing Server Status...")
    
    try:
        status = get_server_status()
        
        required_fields = ["status", "version", "type", "system_info", "capabilities"]
        missing_fields = [field for field in required_fields if field not in status]
        
        if missing_fields:
            print(f"  ❌ Missing fields: {missing_fields}")
            return False
        
        print(f"  ✅ Status: {status['status']}")
        print(f"  ✅ Version: {status['version']}")
        print(f"  ✅ Type: {status['type']}")
        print(f"  ✅ Capabilities: {len(status['capabilities'])} items")
        
        print("📊 Server Status: SUCCESS\n")
        return True
        
    except Exception as e:
        print(f"  ❌ Server status failed: {e}")
        print("📊 Server Status: FAILED\n")
        return False


async def test_workflow_simulation():
    """Test a simulated user interaction workflow using Client."""
    print("🔄 Testing Workflow Simulation...")
    
    try:
        # Create server
        mcp = FastMCP("Workflow Test Server")
        register_prompts(mcp)
        register_tools(mcp)
        
        # Simulate recipe creation workflow
        print("  🍳 Simulating recipe creation workflow...")
        
        async with Client(mcp) as client:
            # Step 1: Get recipe name
            name_result = await client.call_tool(
                "get_user_input",
                {
                    "title": "Recipe Creator",
                    "prompt": "What would you like to name your recipe?",
                    "default_value": "My Recipe"
                }
            )
            if name_result.is_error or not name_result.data.get("success"):
                print(f"  ❌ Recipe name step failed: {name_result.data}")
                return False
            print("    ✅ Recipe name prompt prepared")
            
            # Step 2: Choose cuisine
            cuisine_result = await client.call_tool(
                "get_user_choice",
                {
                    "title": "Cuisine Selection",
                    "prompt": "What type of cuisine is this recipe?",
                    "choices": ["Italian", "Mexican", "Asian", "American", "Other"]
                }
            )
            if cuisine_result.is_error or not cuisine_result.data.get("success"):
                print(f"  ❌ Cuisine choice step failed: {cuisine_result.data}")
                return False
            print("    ✅ Cuisine choice prompt prepared")
            
            # Step 3: Get ingredients
            ingredients_result = await client.call_tool(
                "get_multiline_input",
                {
                    "title": "Recipe Ingredients",
                    "prompt": "Please list all ingredients:",
                    "placeholder": "1 cup flour\n2 eggs\n1 tsp salt"
                }
            )
            if ingredients_result.is_error or not ingredients_result.data.get("success"):
                print(f"  ❌ Ingredients step failed: {ingredients_result.data}")
                return False
            print("    ✅ Ingredients input prompt prepared")
            
            # Step 4: Show completion
            completion_result = await client.call_tool(
                "show_info_message",
                {
                    "title": "Recipe Created",
                    "message": "Your recipe has been prepared successfully!",
                    "info_type": "success"
                }
            )
            if completion_result.is_error or not completion_result.data.get("success"):
                print(f"  ❌ Completion step failed: {completion_result.data}")
                return False
            print("    ✅ Completion message prompt prepared")
        
        print("🔄 Workflow Simulation: SUCCESS\n")
        return True
        
    except Exception as e:
        print(f"  ❌ Workflow simulation failed: {e}")
        print("🔄 Workflow Simulation: FAILED\n")
        return False


async def main():
    """Run all tests."""
    print("🚀 Starting Comprehensive Testing of Human-in-the-Loop MCP Server v2.0\n")
    
    # Run all tests
    results = []
    
    results.append(test_response_validation())
    results.append(await test_mcp_server_creation())
    results.append(await test_tool_functionality())
    results.append(await test_prompt_functionality())
    results.append(test_server_status())
    results.append(await test_workflow_simulation())
    
    # Summary
    passed = sum(results)
    total = len(results)
    
    print(f"🏁 Testing Complete: {passed}/{total} test suites passed")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED! The Human-in-the-Loop MCP Server v2.0 is ready!")
        return True
    else:
        print("💥 Some tests failed. Please review the issues above.")
        return False


if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
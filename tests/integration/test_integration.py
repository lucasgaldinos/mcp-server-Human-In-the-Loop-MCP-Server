"""
Real-world integration tests for the Human-in-the-Loop MCP Server v2.0

This module tests realistic scenarios and edge cases.
"""

import pytest
import asyncio
import sys
from pathlib import Path

# Add src to path
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

from fastmcp import FastMCP
from human_in_the_loop.prompts import register_prompts
from human_in_the_loop.tools import register_tools
from human_in_the_loop.utils.helpers import validate_prompt_response


@pytest.fixture
def full_mcp_server():
    """Create a fully configured MCP server for integration testing."""
    mcp = FastMCP("Integration Test Server")
    register_prompts(mcp)
    register_tools(mcp)
    return mcp


class TestResponseValidation:
    """Test user response validation."""
    
    def test_validate_text_response(self):
        """Test validation of text responses."""
        valid, value, error = validate_prompt_response("Hello World", "text")
        assert valid is True
        assert value == "Hello World"
        assert error == ""
    
    def test_validate_integer_response(self):
        """Test validation of integer responses."""
        valid, value, error = validate_prompt_response("42", "integer")
        assert valid is True
        assert value == 42
        assert error == ""
        
        # Test invalid integer
        valid, value, error = validate_prompt_response("not_a_number", "integer")
        assert valid is False
        assert value is None
        assert "Invalid integer format" in error
    
    def test_validate_float_response(self):
        """Test validation of float responses."""
        valid, value, error = validate_prompt_response("3.14", "float")
        assert valid is True
        assert value == 3.14
        assert error == ""
        
        # Test invalid float
        valid, value, error = validate_prompt_response("not_a_float", "float")
        assert valid is False
        assert value is None
        assert "Invalid float format" in error
    
    def test_validate_choice_response_numeric(self):
        """Test validation of numeric choice responses."""
        valid, value, error = validate_prompt_response("2", "choice")
        assert valid is True
        assert value == 2
        assert error == ""
    
    def test_validate_choice_response_text(self):
        """Test validation of text choice responses."""
        valid, value, error = validate_prompt_response("Option A", "choice")
        assert valid is True
        assert value == "Option A"
        assert error == ""
    
    def test_validate_choice_response_multiple(self):
        """Test validation of multiple choice responses."""
        valid, value, error = validate_prompt_response("1, 3, 5", "choice")
        assert valid is True
        assert value == [1, 3, 5]
        assert error == ""
        
        # Test mixed numeric and text
        valid, value, error = validate_prompt_response("1, Option B, 3", "choice")
        assert valid is True
        assert value == [1, "Option B", 3]
        assert error == ""
    
    def test_validate_confirmation_response(self):
        """Test validation of confirmation responses."""
        # Test positive responses
        for response in ["yes", "y", "true", "confirm", "ok", "1"]:
            valid, value, error = validate_prompt_response(response, "confirmation")
            assert valid is True
            assert value is True
            assert error == ""
        
        # Test negative responses
        for response in ["no", "n", "false", "cancel", "deny", "0"]:
            valid, value, error = validate_prompt_response(response, "confirmation")
            assert valid is True
            assert value is False
            assert error == ""
        
        # Test invalid confirmation
        valid, value, error = validate_prompt_response("maybe", "confirmation")
        assert valid is False
        assert value is None
        assert "Invalid confirmation response" in error
    
    def test_validate_empty_response(self):
        """Test validation of empty responses."""
        for response_type in ["text", "integer", "float", "choice", "confirmation"]:
            valid, value, error = validate_prompt_response("", response_type)
            assert valid is False
            assert value is None
            assert "Empty response provided" in error


class TestRealWorldScenarios:
    """Test realistic usage scenarios."""
    
    @pytest.mark.asyncio
    async def test_recipe_creation_workflow(self, full_mcp_server):
        """Test a recipe creation workflow."""
        tools = full_mcp_server._tool_manager._tools
        
        # Find tools
        get_user_input = None
        get_user_choice = None
        get_multiline_input = None
        show_info_message = None
        
        for tool_name, tool_func in tools.items():
            if "get_user_input" in tool_name and get_user_input is None:
                get_user_input = tool_func
            elif "get_user_choice" in tool_name and get_user_choice is None:
                get_user_choice = tool_func
            elif "get_multiline_input" in tool_name and get_multiline_input is None:
                get_multiline_input = tool_func
            elif "show_info_message" in tool_name and show_info_message is None:
                show_info_message = tool_func
        
        # Step 1: Get recipe name
        name_result = await get_user_input(
            title="Recipe Creator",
            prompt="What would you like to name your recipe?",
            default_value="My Recipe"
        )
        assert name_result["success"] is True
        assert name_result["prompt_type"] == "get_user_input_prompt"
        
        # Step 2: Choose cuisine type
        cuisine_result = await get_user_choice(
            title="Cuisine Selection",
            prompt="What type of cuisine is this recipe?",
            choices=["Italian", "Mexican", "Asian", "American", "Other"]
        )
        assert cuisine_result["success"] is True
        assert cuisine_result["choice_count"] == 5
        
        # Step 3: Get ingredients
        ingredients_result = await get_multiline_input(
            title="Recipe Ingredients",
            prompt="Please list all ingredients (one per line):",
            placeholder="1 cup flour\n2 eggs\n1 tsp salt"
        )
        assert ingredients_result["success"] is True
        assert ingredients_result["expects_multiline"] is True
        
        # Step 4: Get instructions
        instructions_result = await get_multiline_input(
            title="Cooking Instructions",
            prompt="Please provide step-by-step cooking instructions:",
            placeholder="1. Preheat oven to 350°F\n2. Mix dry ingredients..."
        )
        assert instructions_result["success"] is True
        
        # Step 5: Show completion message
        completion_result = await show_info_message(
            title="Recipe Created",
            message="Your recipe has been prepared! The prompts will guide you through entering all the details.",
            info_type="success"
        )
        assert completion_result["success"] is True
        assert completion_result["message_type"] == "success"
    
    @pytest.mark.asyncio
    async def test_file_management_workflow(self, full_mcp_server):
        """Test a file management workflow."""
        tools = full_mcp_server._tool_manager._tools
        
        get_user_choice = None
        show_confirmation_dialog = None
        show_info_message = None
        
        for tool_name, tool_func in tools.items():
            if "get_user_choice" in tool_name and get_user_choice is None:
                get_user_choice = tool_func
            elif "show_confirmation_dialog" in tool_name and show_confirmation_dialog is None:
                show_confirmation_dialog = tool_func
            elif "show_info_message" in tool_name and show_info_message is None:
                show_info_message = tool_func
        
        # Step 1: Choose action
        action_result = await get_user_choice(
            title="File Manager",
            prompt="What would you like to do?",
            choices=["Delete old files", "Backup important files", "Organize by date", "Clean temporary files"]
        )
        assert action_result["success"] is True
        
        # Step 2: Confirm potentially destructive action
        confirm_result = await show_confirmation_dialog(
            title="Confirm Action",
            message="This action may modify or delete files. Are you sure you want to proceed?",
            confirm_text="Proceed",
            cancel_text="Cancel"
        )
        assert confirm_result["success"] is True
        assert confirm_result["expects_confirmation"] is True
        
        # Step 3: Show status
        status_result = await show_info_message(
            title="Operation Status",
            message="File management operation has been prepared. Please follow the prompts to complete the action.",
            info_type="info"
        )
        assert status_result["success"] is True
    
    @pytest.mark.asyncio
    async def test_configuration_setup_workflow(self, full_mcp_server):
        """Test a configuration setup workflow."""
        tools = full_mcp_server._tool_manager._tools
        
        get_user_input = None
        get_user_choice = None
        show_info_message = None
        
        for tool_name, tool_func in tools.items():
            if "get_user_input" in tool_name and get_user_input is None:
                get_user_input = tool_func
            elif "get_user_choice" in tool_name and get_user_choice is None:
                get_user_choice = tool_func
            elif "show_info_message" in tool_name and show_info_message is None:
                show_info_message = tool_func
        
        # Step 1: Get server URL
        url_result = await get_user_input(
            title="Server Configuration",
            prompt="Enter the server URL:",
            default_value="https://api.example.com",
            input_type="text"
        )
        assert url_result["success"] is True
        
        # Step 2: Get port number
        port_result = await get_user_input(
            title="Port Configuration",
            prompt="Enter the port number:",
            default_value="8080",
            input_type="integer"
        )
        assert port_result["success"] is True
        assert port_result["input_type"] == "integer"
        
        # Step 3: Choose protocol
        protocol_result = await get_user_choice(
            title="Protocol Selection",
            prompt="Select the connection protocol:",
            choices=["HTTP", "HTTPS", "WebSocket", "TCP"]
        )
        assert protocol_result["success"] is True
        
        # Step 4: Show completion
        completion_result = await show_info_message(
            title="Configuration Complete",
            message="Server configuration has been prepared. Use the prompts to provide all necessary details.",
            info_type="success"
        )
        assert completion_result["success"] is True


class TestErrorHandling:
    """Test error handling scenarios."""
    
    @pytest.mark.asyncio
    async def test_invalid_choice_count(self, full_mcp_server):
        """Test handling of invalid choice counts."""
        tools = full_mcp_server._tool_manager._tools
        
        get_user_choice = None
        for tool_name, tool_func in tools.items():
            if "get_user_choice" in tool_name:
                get_user_choice = tool_func
                break
        
        # Test with empty choices
        result = await get_user_choice(
            title="Invalid Choice",
            prompt="Select from no options:",
            choices=[]
        )
        
        assert result["success"] is False
        assert "No choices provided" in result["error"]
    
    @pytest.mark.asyncio
    async def test_tool_parameter_validation(self, full_mcp_server):
        """Test parameter validation in tools."""
        tools = full_mcp_server._tool_manager._tools
        
        get_user_input = None
        for tool_name, tool_func in tools.items():
            if "get_user_input" in tool_name:
                get_user_input = tool_func
                break
        
        # Test with valid parameters - should succeed
        result = await get_user_input(
            title="Valid Test",
            prompt="Enter something:",
            default_value="default",
            input_type="text"
        )
        
        assert result["success"] is True


class TestHealthCheck:
    """Test health check functionality."""
    
    @pytest.mark.asyncio
    async def test_comprehensive_health_check(self, full_mcp_server):
        """Test comprehensive health check."""
        tools = full_mcp_server._tool_manager._tools
        
        health_check = None
        for tool_name, tool_func in tools.items():
            if "health_check" in tool_name:
                health_check = tool_func
                break
        
        result = await health_check()
        
        # Verify all expected fields
        assert result["success"] is True
        assert result["status"] == "healthy"
        assert result["server_type"] == "Human-in-the-Loop MCP Server"
        assert result["version"] == "2.0.0"
        assert result["interaction_method"] == "MCP Prompts"
        assert result["ready"] is True
        
        # Verify capabilities
        capabilities = result["capabilities"]
        assert "prompts" in capabilities
        assert "tools" in capabilities
        
        # Verify system info
        system_info = result["system_info"]
        assert "platform" in system_info
        assert "python_version" in system_info
        assert "server_time" in system_info
        
        # Verify counts
        assert result["prompt_count"] == 5
        assert result["tool_count"] == 6


if __name__ == "__main__":
    # Run integration tests
    pytest.main([__file__, "-v"])
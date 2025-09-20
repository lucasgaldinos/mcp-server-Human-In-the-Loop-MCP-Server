"""
Comprehensive tests for the Human-in-the-Loop MCP Server v2.0

This module tests all prompt-based tools and their functionality.
"""

import pytest
import asyncio
import sys
from pathlib import Path
from unittest.mock import AsyncMock, patch

# Add src to path for testing
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

from fastmcp import FastMCP, Context
from human_in_the_loop.prompts import register_prompts
from human_in_the_loop.tools import register_tools
from human_in_the_loop.utils.error_handling import (
    validate_prompt_params,
    PromptValidationError,
    create_error_response,
    create_success_response
)


@pytest.fixture
def mcp_server():
    """Create a test MCP server with all prompts and tools registered."""
    mcp = FastMCP("Test Human-in-the-Loop Server")
    register_prompts(mcp)
    register_tools(mcp)
    return mcp


@pytest.fixture
def mock_context():
    """Create a mock MCP context for testing."""
    context = AsyncMock(spec=Context)
    context.info = AsyncMock()
    context.debug = AsyncMock()
    context.error = AsyncMock()
    return context


class TestPromptValidation:
    """Test prompt parameter validation."""
    
    def test_validate_required_fields_success(self):
        """Test successful validation with all required fields."""
        params = {
            "title": "Test Title",
            "prompt": "Test prompt",
            "choices": ["Option 1", "Option 2"]
        }
        required = ["title", "prompt", "choices"]
        
        # Should not raise any exception
        validate_prompt_params(params, required)
    
    def test_validate_missing_required_field(self):
        """Test validation failure with missing required field."""
        params = {
            "title": "Test Title",
            "prompt": "Test prompt"
            # Missing 'choices'
        }
        required = ["title", "prompt", "choices"]
        
        with pytest.raises(PromptValidationError, match="Missing required fields: choices"):
            validate_prompt_params(params, required)
    
    def test_validate_invalid_title_type(self):
        """Test validation failure with invalid title type."""
        params = {
            "title": 123,  # Should be string
            "prompt": "Test prompt"
        }
        required = ["title", "prompt"]
        
        with pytest.raises(PromptValidationError, match="Title must be a string"):
            validate_prompt_params(params, required)
    
    def test_validate_empty_choices_list(self):
        """Test validation failure with empty choices list."""
        params = {
            "title": "Test Title",
            "prompt": "Test prompt",
            "choices": []  # Empty list
        }
        required = ["title", "prompt", "choices"]
        
        with pytest.raises(PromptValidationError, match="Choices list cannot be empty"):
            validate_prompt_params(params, required)


class TestErrorResponses:
    """Test error response creation."""
    
    def test_create_error_response(self):
        """Test error response creation."""
        response = create_error_response("Test error", "validation", extra_field="value")
        
        assert response["success"] is False
        assert response["error"] == "Test error"
        assert response["error_type"] == "validation"
        assert response["prompt_required"] is False
        assert "timestamp" in response
        assert response["extra_field"] == "value"
    
    def test_create_success_response(self):
        """Test success response creation."""
        data = {"result": "test", "value": 42}
        response = create_success_response(data)
        
        assert response["success"] is True
        assert response["result"] == "test"
        assert response["value"] == 42
        assert "timestamp" in response


class TestMCPTools:
    """Test MCP tool implementations."""
    
    @pytest.mark.asyncio
    async def test_get_user_input_tool(self, mcp_server, mock_context):
        """Test get_user_input tool functionality."""
        # Get the tool function from the registered tools
        tools = mcp_server._tool_manager._tools
        get_user_input = None
        
        for tool_name, tool_func in tools.items():
            if "get_user_input" in tool_name:
                get_user_input = tool_func
                break
        
        assert get_user_input is not None, "get_user_input tool not found"
        
        # Test with valid parameters
        result = await get_user_input(
            title="Test Input",
            prompt="Enter a value:",
            default_value="default",
            input_type="text",
            ctx=mock_context
        )
        
        assert result["success"] is True
        assert result["prompt_required"] is True
        assert result["prompt_type"] == "get_user_input_prompt"
        assert result["prompt_params"]["title"] == "Test Input"
        assert result["prompt_params"]["prompt"] == "Enter a value:"
        assert result["input_type"] == "text"
        assert result["expects_response"] is True
    
    @pytest.mark.asyncio
    async def test_get_user_choice_tool(self, mcp_server, mock_context):
        """Test get_user_choice tool functionality."""
        tools = mcp_server._tool_manager._tools
        get_user_choice = None
        
        for tool_name, tool_func in tools.items():
            if "get_user_choice" in tool_name:
                get_user_choice = tool_func
                break
        
        assert get_user_choice is not None, "get_user_choice tool not found"
        
        # Test with valid parameters
        choices = ["Option 1", "Option 2", "Option 3"]
        result = await get_user_choice(
            title="Test Choice",
            prompt="Select an option:",
            choices=choices,
            allow_multiple=False,
            ctx=mock_context
        )
        
        assert result["success"] is True
        assert result["prompt_required"] is True
        assert result["prompt_type"] == "get_user_choice_prompt"
        assert result["prompt_params"]["choices"] == choices
        assert result["choice_count"] == 3
        assert result["allow_multiple"] is False
    
    @pytest.mark.asyncio
    async def test_get_user_choice_empty_choices(self, mcp_server, mock_context):
        """Test get_user_choice tool with empty choices list."""
        tools = mcp_server._tool_manager._tools
        get_user_choice = None
        
        for tool_name, tool_func in tools.items():
            if "get_user_choice" in tool_name:
                get_user_choice = tool_func
                break
        
        # Test with empty choices
        result = await get_user_choice(
            title="Test Choice",
            prompt="Select an option:",
            choices=[],
            ctx=mock_context
        )
        
        assert result["success"] is False
        assert result["prompt_required"] is False
        assert "No choices provided" in result["error"]
    
    @pytest.mark.asyncio
    async def test_get_multiline_input_tool(self, mcp_server, mock_context):
        """Test get_multiline_input tool functionality."""
        tools = mcp_server._tool_manager._tools
        get_multiline_input = None
        
        for tool_name, tool_func in tools.items():
            if "get_multiline_input" in tool_name:
                get_multiline_input = tool_func
                break
        
        assert get_multiline_input is not None, "get_multiline_input tool not found"
        
        result = await get_multiline_input(
            title="Test Multiline",
            prompt="Enter detailed text:",
            default_value="Default content",
            placeholder="Enter your text here...",
            ctx=mock_context
        )
        
        assert result["success"] is True
        assert result["prompt_required"] is True
        assert result["prompt_type"] == "get_multiline_input_prompt"
        assert result["expects_multiline"] is True
    
    @pytest.mark.asyncio
    async def test_show_confirmation_dialog_tool(self, mcp_server, mock_context):
        """Test show_confirmation_dialog tool functionality."""
        tools = mcp_server._tool_manager._tools
        show_confirmation_dialog = None
        
        for tool_name, tool_func in tools.items():
            if "show_confirmation_dialog" in tool_name:
                show_confirmation_dialog = tool_func
                break
        
        assert show_confirmation_dialog is not None, "show_confirmation_dialog tool not found"
        
        result = await show_confirmation_dialog(
            title="Confirm Action",
            message="Are you sure you want to proceed?",
            confirm_text="Proceed",
            cancel_text="Cancel",
            ctx=mock_context
        )
        
        assert result["success"] is True
        assert result["prompt_required"] is True
        assert result["prompt_type"] == "show_confirmation_prompt"
        assert result["expects_confirmation"] is True
    
    @pytest.mark.asyncio
    async def test_show_info_message_tool(self, mcp_server, mock_context):
        """Test show_info_message tool functionality."""
        tools = mcp_server._tool_manager._tools
        show_info_message = None
        
        for tool_name, tool_func in tools.items():
            if "show_info_message" in tool_name:
                show_info_message = tool_func
                break
        
        assert show_info_message is not None, "show_info_message tool not found"
        
        result = await show_info_message(
            title="Information",
            message="Operation completed successfully!",
            info_type="success",
            ctx=mock_context
        )
        
        assert result["success"] is True
        assert result["prompt_required"] is True
        assert result["prompt_type"] == "show_info_message_prompt"
        assert result["message_type"] == "success"
        assert result["expects_acknowledgment"] is True
    
    @pytest.mark.asyncio
    async def test_health_check_tool(self, mcp_server, mock_context):
        """Test health_check tool functionality."""
        tools = mcp_server._tool_manager._tools
        health_check = None
        
        for tool_name, tool_func in tools.items():
            if "health_check" in tool_name:
                health_check = tool_func
                break
        
        assert health_check is not None, "health_check tool not found"
        
        result = await health_check(ctx=mock_context)
        
        assert result["success"] is True
        assert result["status"] == "healthy"
        assert result["server_type"] == "Human-in-the-Loop MCP Server"
        assert result["version"] == "2.0.0"
        assert result["interaction_method"] == "MCP Prompts"
        assert result["ready"] is True
        assert "capabilities" in result
        assert "system_info" in result


class TestMCPPrompts:
    """Test MCP prompt implementations."""
    
    @pytest.mark.asyncio
    async def test_get_user_input_prompt(self, mcp_server):
        """Test get_user_input_prompt functionality."""
        prompts = mcp_server._prompt_manager._prompts
        user_input_prompt = None
        
        for prompt_name, prompt_func in prompts.items():
            if "get_user_input_prompt" in prompt_name:
                user_input_prompt = prompt_func
                break
        
        assert user_input_prompt is not None, "get_user_input_prompt not found"
        
        result = await user_input_prompt(
            title="Test Input",
            prompt="Enter a value:",
            default_value="default",
            input_type="text"
        )
        
        assert "content" in result
        assert "Test Input" in result["content"]
        assert "Enter a value:" in result["content"]
        assert "text" in result["content"]
    
    @pytest.mark.asyncio
    async def test_get_user_choice_prompt(self, mcp_server):
        """Test get_user_choice_prompt functionality."""
        prompts = mcp_server._prompt_manager._prompts
        user_choice_prompt = None
        
        for prompt_name, prompt_func in prompts.items():
            if "get_user_choice_prompt" in prompt_name:
                user_choice_prompt = prompt_func
                break
        
        assert user_choice_prompt is not None, "get_user_choice_prompt not found"
        
        choices = ["Option 1", "Option 2", "Option 3"]
        result = await user_choice_prompt(
            title="Test Choice",
            prompt="Select an option:",
            choices=choices,
            allow_multiple=False
        )
        
        assert "content" in result
        assert "Test Choice" in result["content"]
        assert "Select an option:" in result["content"]
        assert "1. Option 1" in result["content"]
        assert "2. Option 2" in result["content"]
        assert "3. Option 3" in result["content"]


class TestIntegrationWorkflows:
    """Test complete workflows that combine multiple tools."""
    
    @pytest.mark.asyncio
    async def test_survey_workflow(self, mcp_server, mock_context):
        """Test a complete survey workflow using multiple tools."""
        tools = mcp_server._tool_manager._tools
        
        # Find tools
        get_user_input = None
        get_user_choice = None
        show_info_message = None
        
        for tool_name, tool_func in tools.items():
            if "get_user_input" in tool_name:
                get_user_input = tool_func
            elif "get_user_choice" in tool_name:
                get_user_choice = tool_func
            elif "show_info_message" in tool_name:
                show_info_message = tool_func
        
        # Step 1: Get user's name
        name_result = await get_user_input(
            title="User Survey",
            prompt="What is your name?",
            ctx=mock_context
        )
        assert name_result["success"] is True
        
        # Step 2: Get user's preference
        choice_result = await get_user_choice(
            title="Preference Selection",
            prompt="What is your favorite color?",
            choices=["Red", "Blue", "Green", "Yellow"],
            ctx=mock_context
        )
        assert choice_result["success"] is True
        
        # Step 3: Show completion message
        info_result = await show_info_message(
            title="Survey Complete",
            message="Thank you for completing the survey!",
            info_type="success",
            ctx=mock_context
        )
        assert info_result["success"] is True
    
    @pytest.mark.asyncio
    async def test_confirmation_workflow(self, mcp_server, mock_context):
        """Test a workflow that requires user confirmation."""
        tools = mcp_server._tool_manager._tools
        
        show_confirmation_dialog = None
        show_info_message = None
        
        for tool_name, tool_func in tools.items():
            if "show_confirmation_dialog" in tool_name:
                show_confirmation_dialog = tool_func
            elif "show_info_message" in tool_name:
                show_info_message = tool_func
        
        # Step 1: Ask for confirmation
        confirm_result = await show_confirmation_dialog(
            title="Delete Files",
            message="Are you sure you want to delete all temporary files?",
            confirm_text="Delete",
            cancel_text="Keep",
            ctx=mock_context
        )
        assert confirm_result["success"] is True
        
        # Step 2: Show result message
        info_result = await show_info_message(
            title="Operation Status",
            message="Deletion confirmation has been prepared.",
            info_type="info",
            ctx=mock_context
        )
        assert info_result["success"] is True


if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v"])
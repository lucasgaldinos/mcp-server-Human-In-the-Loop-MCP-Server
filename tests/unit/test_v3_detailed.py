#!/usr/bin/env python3
"""
Detailed tool registration test for MCP v3.0 Human-in-the-Loop Server
"""

import asyncio
import sys
import logging
from typing import Dict, Any

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

async def test_tool_registration():
    """Test detailed tool registration"""
    try:
        logger.info("🔍 Testing tool registration in detail...")
        
        # Import the server module 
        from human_loop_server_v3 import mcp
        
        # Check various attributes for tools
        attributes_to_check = [
            '_tools',
            'tools', 
            '_tool_manager',
            'tool_manager',
            '_functions',
            'functions'
        ]
        
        logger.info(f"MCP instance type: {type(mcp)}")
        logger.info(f"MCP instance name: {getattr(mcp, 'name', 'NO NAME')}")
        
        for attr in attributes_to_check:
            if hasattr(mcp, attr):
                value = getattr(mcp, attr)
                logger.info(f"✅ Found attribute '{attr}': {type(value)}")
                
                if hasattr(value, '__len__'):
                    try:
                        length = len(value)
                        logger.info(f"   Length: {length}")
                        if length > 0:
                            if hasattr(value, 'keys'):
                                logger.info(f"   Keys: {list(value.keys())}")
                            elif hasattr(value, '__iter__'):
                                logger.info(f"   Items: {list(value)[:5]}")  # First 5 items
                    except Exception as e:
                        logger.info(f"   Could not get length: {e}")
                        
                if hasattr(value, 'list_tools'):
                    try:
                        tools = value.list_tools()
                        logger.info(f"   list_tools() returned: {len(tools)} tools")
                        for tool in tools:
                            logger.info(f"     - {getattr(tool, 'name', 'NO NAME')}")
                    except Exception as e:
                        logger.info(f"   list_tools() failed: {e}")
                        
            else:
                logger.info(f"❌ No attribute '{attr}'")
        
        # Check if we can manually call the decorated functions
        logger.info("\n🔍 Testing if tool functions exist as module attributes...")
        
        import human_loop_server_v3 as server_module
        tool_functions = [
            'health_check',
            'get_user_input', 
            'get_user_choice',
            'get_multiline_input',
            'show_confirmation_dialog',
            'show_info_message'
        ]
        
        for func_name in tool_functions:
            if hasattr(server_module, func_name):
                func = getattr(server_module, func_name)
                logger.info(f"✅ Found function '{func_name}': {type(func)}")
                
                # Check if it's async
                if asyncio.iscoroutinefunction(func):
                    logger.info(f"   '{func_name}' is async")
                else:
                    logger.info(f"   '{func_name}' is sync")
                    
                # Check docstring
                if func.__doc__:
                    logger.info(f"   Docstring: {func.__doc__[:100]}...")
            else:
                logger.error(f"❌ Missing function '{func_name}'")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Error testing tool registration: {e}")
        import traceback
        traceback.print_exc()
        return False

async def test_fastmcp_info():
    """Get FastMCP version and info"""
    try:
        logger.info("🔍 Testing FastMCP version and configuration...")
        
        import fastmcp
        if hasattr(fastmcp, '__version__'):
            logger.info(f"FastMCP version: {fastmcp.__version__}")
        
        from mcp.server.fastmcp import FastMCP
        
        # Create a simple test instance to see how tool registration works
        test_mcp = FastMCP("TestServer")
        
        @test_mcp.tool()
        def test_function() -> str:
            """Test function"""
            return "test"
        
        logger.info(f"Test MCP instance created: {test_mcp.name}")
        
        # Check if the test tool was registered
        if hasattr(test_mcp, '_tools'):
            tools = test_mcp._tools
            logger.info(f"Test MCP tools: {len(tools)} found")
            for name, tool in tools.items():
                logger.info(f"  - {name}: {type(tool)}")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Error testing FastMCP info: {e}")
        import traceback
        traceback.print_exc()
        return False

async def main():
    """Run detailed tool registration tests"""
    logger.info("🧪 Starting Detailed Tool Registration Tests")
    logger.info("=" * 70)
    
    tests = [
        ("FastMCP Info Test", test_fastmcp_info),
        ("Tool Registration Test", test_tool_registration),
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        logger.info(f"\n🔍 Running: {test_name}")
        logger.info("-" * 50)
        try:
            result = await test_func()
            results[test_name] = result
            if result:
                logger.info(f"✅ {test_name}: PASSED")
            else:
                logger.error(f"❌ {test_name}: FAILED")
        except Exception as e:
            logger.error(f"❌ {test_name}: FAILED with exception: {e}")
            results[test_name] = False
    
    # Summary
    logger.info("\n" + "=" * 70)
    logger.info("📊 DETAILED TEST SUMMARY")
    logger.info("=" * 70)
    
    passed = sum(1 for result in results.values() if result)
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        logger.info(f"{status}: {test_name}")
    
    logger.info(f"\n🎯 Overall: {passed}/{total} tests passed")
    
    return passed == total

if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
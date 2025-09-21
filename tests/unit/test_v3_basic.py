#!/usr/bin/env python3
"""
Test script for MCP v3.0 Human-in-the-Loop Server
Tests basic functionality without running the full server
"""

import asyncio
import sys
import logging
from typing import Dict, Any

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

async def test_import():
    """Test if we can import the server module"""
    try:
        from human_loop_server_v3 import mcp, health_check
        logger.info("✅ Successfully imported server module")
        return True
    except Exception as e:
        logger.error(f"❌ Failed to import server module: {e}")
        return False

async def test_mcp_instance():
    """Test if MCP instance is properly created"""
    try:
        from human_loop_server_v3 import mcp
        logger.info(f"✅ MCP instance created: {mcp.name}")
        
        # Check if tools are registered
        if hasattr(mcp, '_tools') and mcp._tools:
            logger.info(f"✅ Found {len(mcp._tools)} registered tools")
            for tool_name in mcp._tools.keys():
                logger.info(f"  - {tool_name}")
        else:
            logger.warning("⚠️ No tools found in MCP instance")
        
        return True
    except Exception as e:
        logger.error(f"❌ Failed to access MCP instance: {e}")
        return False

async def test_elicitation_imports():
    """Test if elicitation-related imports work"""
    try:
        from mcp.server.fastmcp import FastMCP, Context
        logger.info("✅ FastMCP and Context imports successful")
        return True
    except Exception as e:
        logger.error(f"❌ Failed to import elicitation components: {e}")
        return False

async def main():
    """Run all basic tests"""
    logger.info("🧪 Starting MCP v3.0 Basic Functionality Tests")
    logger.info("=" * 60)
    
    tests = [
        ("Import Test", test_import),
        ("MCP Instance Test", test_mcp_instance), 
        ("Elicitation Imports Test", test_elicitation_imports),
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        logger.info(f"\n🔍 Running: {test_name}")
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
    logger.info("\n" + "=" * 60)
    logger.info("📊 TEST SUMMARY")
    logger.info("=" * 60)
    
    passed = sum(1 for result in results.values() if result)
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        logger.info(f"{status}: {test_name}")
    
    logger.info(f"\n🎯 Overall: {passed}/{total} tests passed")
    
    if passed == total:
        logger.info("🎉 All basic tests passed! Server is ready for MCP testing.")
        return True
    else:
        logger.error("⚠️ Some tests failed. Check server configuration.")
        return False

if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
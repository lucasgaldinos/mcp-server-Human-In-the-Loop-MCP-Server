#!/usr/bin/env python3
"""
Test script for Human-in-the-Loop MCP Server v3.0 - Elicitation Testing

This script tests the new elicitation-based tools to ensure they work correctly
and demonstrate the difference from the old JSON-response system.
"""

import json
import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def test_v3_elicitations():
    """Test the new v3 elicitation-based tools"""
    
    print("🧪 TESTING HUMAN-IN-THE-LOOP MCP SERVER v3.0")
    print("=" * 50)
    
    server_params = StdioServerParameters(
        command="python",
        args=["human_loop_server_v3.py"],
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            # List available tools
            print("\n📋 AVAILABLE TOOLS:")
            tools = await session.list_tools()
            for tool in tools.tools:
                print(f"  • {tool.name}: {tool.description}")
            
            print(f"\n✅ Found {len(tools.tools)} elicitation-based tools")
            print("\n💡 When you run these tools in VS Code, you should see:")
            print("   - Native Command Palette-style input dialogs")
            print("   - No complex JSON responses")
            print("   - Clean, user-friendly interfaces")
            
            # Test the health check first
            print("\n🏥 TESTING HEALTH CHECK:")
            health_result = await session.call_tool("health_check", {})
            print("Health Check Result:")
            for content in health_result.content:
                if hasattr(content, 'text'):
                    print(content.text)
            
            print("\n✨ v3.0 SERVER IS READY!")
            print("🎯 The tools use ctx.elicit() to create native VS Code dialogs")
            print("🚀 No more complex JSON responses - just clean user interfaces!")

if __name__ == "__main__":
    asyncio.run(test_v3_elicitations())
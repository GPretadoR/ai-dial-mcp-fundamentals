import asyncio
import json
import os

from mcp import Resource
from mcp.types import Prompt

from agent.mcp_client import MCPClient
from agent.dial_client import DialClient
from agent.models.message import Message, Role
from agent.prompts import SYSTEM_PROMPT


# https://remote.mcpservers.org/fetch/mcp
# Pay attention that `fetch` doesn't have resources and prompts

async def main():
    # Get environment variables
    dial_api_key = os.getenv("DIAL_API_KEY")
    if not dial_api_key:
        print("❌ Error: DIAL_API_KEY environment variable is not set")
        print("Please set it using: export DIAL_API_KEY='your-api-key-here'")
        return
    
    dial_endpoint = os.getenv("DIAL_ENDPOINT", "https://dial.api.epam.com/openai/deployments/")
    
    print("=" * 80)
    print("🚀 Starting Users Management Agent")
    print("=" * 80)
    
    # Create MCP client and open connection to the MCP server
    async with MCPClient(mcp_server_url="http://localhost:8005/mcp") as mcp_client:
        
        # Get available MCP Resources and print them
        print("\n📚 Fetching MCP Resources...")
        resources = await mcp_client.get_resources()
        if resources:
            print(f"✅ Found {len(resources)} resource(s):")
            for resource in resources:
                print(f"   - {resource.uri}: {resource.name}")
        else:
            print("   No resources available")
        
        # Get available MCP Tools and print them
        print("\n🛠️  Fetching MCP Tools...")
        tools = await mcp_client.get_tools()
        if tools:
            print(f"✅ Found {len(tools)} tool(s):")
            for tool in tools:
                tool_name = tool["function"]["name"]
                tool_desc = tool["function"]["description"]
                print(f"   - {tool_name}: {tool_desc[:80]}...")
        else:
            print("   No tools available")
            return
        
        # Create DialClient
        print("\n🌐 Initializing DIAL Client...")
        dial_client = DialClient(
            api_key=dial_api_key,
            endpoint=dial_endpoint,
            tools=tools,
            mcp_client=mcp_client
        )
        print("✅ DIAL Client ready")
        
        # Create list with messages and add SYSTEM_PROMPT
        messages = [Message(role=Role.SYSTEM, content=SYSTEM_PROMPT)]
        
        # Add MCP prompts to messages as User messages
        print("\n📝 Fetching MCP Prompts...")
        prompts = await mcp_client.get_prompts()
        if prompts:
            print(f"✅ Found {len(prompts)} prompt(s):")
            for prompt in prompts:
                print(f"   - {prompt.name}: {prompt.description[:60] if prompt.description else 'No description'}...")
                # Get full prompt content and add to messages
                prompt_content = await mcp_client.get_prompt(prompt.name)
                messages.append(Message(role=Role.USER, content=prompt_content))
        else:
            print("   No prompts available")
        
        # Create console chat
        print("\n" + "=" * 80)
        print("💬 Chat Interface Ready")
        print("=" * 80)
        print("You can now interact with the Users Management Agent.")
        print("Type 'exit' or 'quit' to end the conversation.")
        print("=" * 80 + "\n")
        
        # Infinite loop with ability to exit and preserve message history
        while True:
            try:
                # Get user input
                user_input = input("👤 You: ").strip()
                
                # Check for exit commands
                if user_input.lower() in ["exit", "quit", "q"]:
                    print("\n👋 Goodbye! Thanks for using the Users Management Agent.")
                    break
                
                # Skip empty inputs
                if not user_input:
                    continue
                
                # Add user message to conversation history
                messages.append(Message(role=Role.USER, content=user_input))
                
                # Get AI response with tool execution
                ai_response = await dial_client.get_completion(messages)
                
                # Add AI response to conversation history
                messages.append(ai_response)
                
                print()  # Add blank line for readability
                
            except KeyboardInterrupt:
                print("\n\n👋 Interrupted. Goodbye!")
                break
            except Exception as e:
                print(f"\n❌ Error: {str(e)}")
                print("Please try again or type 'exit' to quit.\n")


if __name__ == "__main__":
    asyncio.run(main())

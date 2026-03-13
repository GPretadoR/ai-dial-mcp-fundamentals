from typing import Optional, Any

from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client
from mcp.types import CallToolResult, TextContent, GetPromptResult, ReadResourceResult, Resource, TextResourceContents, BlobResourceContents, Prompt
from pydantic import AnyUrl


class MCPClient:
    """Handles MCP server connection and tool execution"""

    def __init__(self, mcp_server_url: str) -> None:
        self.mcp_server_url = mcp_server_url
        self.session: Optional[ClientSession] = None
        self._streams_context = None
        self._session_context = None

    async def __aenter__(self):
        # Create streamable HTTP client context
        self._streams_context = streamablehttp_client(self.mcp_server_url)
        
        # Enter streams context and get read/write streams
        read_stream, write_stream, _ = await self._streams_context.__aenter__()
        
        # Create ClientSession with streams
        self._session_context = ClientSession(read_stream, write_stream)
        
        # Enter session context and initialize
        self.session = await self._session_context.__aenter__()
        
        # Initialize session and print server capabilities
        init_result = await self.session.initialize()
        print(f"🔗 Connected to MCP server: {init_result}")
        
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        # Shutdown session context if present
        if self.session and self._session_context:
            await self._session_context.__aexit__(exc_type, exc_val, exc_tb)
        
        # Shutdown streams context if present
        if self._streams_context:
            await self._streams_context.__aexit__(exc_type, exc_val, exc_tb)

    async def get_tools(self) -> list[dict[str, Any]]:
        """Get available tools from MCP server"""
        if not self.session:
            raise RuntimeError("MCP client not connected. Call connect() first.")
        
        # List tools from MCP server
        tools_response = await self.session.list_tools()
        
        # Convert MCP tool schema to OpenAI/DIAL function schema format
        dial_tools = []
        for tool in tools_response.tools:
            dial_tool = {
                "type": "function",
                "function": {
                    "name": tool.name,
                    "description": tool.description or "",
                    "parameters": tool.inputSchema
                }
            }
            dial_tools.append(dial_tool)
        
        return dial_tools

    async def call_tool(self, tool_name: str, tool_args: dict[str, Any]) -> Any:
        """Call a specific tool on the MCP server"""
        if not self.session:
            raise RuntimeError("MCP client not connected. Call connect() first.")

        # Call the tool on MCP server
        tool_result: CallToolResult = await self.session.call_tool(tool_name, tool_args)
        
        # Get first content from result
        content = tool_result.content[0]
        
        # Print tool execution result
        print(f"    ⚙️: {content}\n")
        
        # Return text content if available, otherwise return raw content
        if isinstance(content, TextContent):
            return content.text
        else:
            return content

    async def get_resources(self) -> list[Resource]:
        """Get available resources from MCP server"""
        if not self.session:
            raise RuntimeError("MCP client not connected.")
        
        try:
            # List resources from MCP server
            resources_response = await self.session.list_resources()
            return resources_response.resources
        except Exception as e:
            print(f"⚠️  Error getting resources: {e}")
            return []

    async def get_resource(self, uri: AnyUrl) -> str:
        """Get specific resource content"""
        if not self.session:
            raise RuntimeError("MCP client not connected.")

        # Get resource by URI
        resource_response: ReadResourceResult = await self.session.read_resource(uri)
        
        # Get first content from resource
        content = resource_response.contents[0]
        
        # Return based on content type
        if isinstance(content, TextResourceContents):
            return content.text
        elif isinstance(content, BlobResourceContents):
            return content.blob
        else:
            return str(content)

    async def get_prompts(self) -> list[Prompt]:
        """Get available prompts from MCP server"""
        if not self.session:
            raise RuntimeError("MCP client not connected.")
        
        try:
            # List prompts from MCP server
            prompts_response = await self.session.list_prompts()
            return prompts_response.prompts
        except Exception as e:
            print(f"⚠️  Error getting prompts: {e}")
            return []

    async def get_prompt(self, name: str) -> str:
        """Get specific prompt content"""
        if not self.session:
            raise RuntimeError("MCP client not connected.")
        
        # Get prompt by name
        prompt_response: GetPromptResult = await self.session.get_prompt(name)
        
        # Combine all message contents
        combined_content = ""
        for message in prompt_response.messages:
            if hasattr(message, 'content'):
                if isinstance(message.content, TextContent):
                    combined_content += message.content.text + "\n"
                elif isinstance(message.content, str):
                    combined_content += message.content + "\n"
        
        return combined_content

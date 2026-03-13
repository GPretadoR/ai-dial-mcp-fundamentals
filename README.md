# Framework-based MCP (Server & Client)
Python implementation for building Users Management Agent with MCP tools and MCP server

## 📑 Table of Contents
- [Task Overview](#-task-overview)
- [Learning Goals](#-learning-goals)
- [Key Concepts](#-key-concepts)
- [Architecture](#%EF%B8%8F-architecture)
- [Requirements](#-requirements)
- [Quick Start](#-quick-start)
- [Setup & Installation](#-setup--installation)
- [Tasks](#%EF%B8%8F-tasks)
  - [Create and run MCP server](#create-and-run-mcp-server)
  - [OPTIONAL: Work with MCP server in Postman](#optional-work-with-mcp-server-in-postman)
  - [Create and run Agent](#create-and-run-agent)
  - [OPTIONAL: Support multiple MCP servers](#optional-support-both-users-management-and-fetch-mcp-servers)
- [Testing & Validation](#-testing--validation)
- [Troubleshooting](#-troubleshooting)
- [Branch Information](#-branch-information)

## 🎯 Task Overview

Create and run an MCP server with simple tools. Implement a Users Management Agent with an MCP Client that will use MCP tools from the created server to perform CRUD operations on a User Management Service.

## 🎓 Learning Goals

By exploring and working with this project, you will learn:

- How to configure and implement a simple MCP server with tools, resources, and prompts
- How to configure a client and establish connection to an MCP server
- How to create an AI Agent that uses tools from an MCP server
- Key features of the Model Context Protocol (MCP)
- How MCP enables 1-to-1 client-server communication
- Integration patterns between MCP servers and AI agents

## 🧠 Key Concepts

### What is MCP?
**Model Context Protocol (MCP)** is a standardized protocol that allows AI applications to interact with external tools and data sources. It provides a unified way for AI agents to:
- **Tools**: Execute actions (e.g., CRUD operations on users)
- **Resources**: Access static or dynamic data (e.g., diagrams, documentation)
- **Prompts**: Use predefined prompt templates

### MCP Architecture Basics
- **1-to-1 Connection**: Each MCP client maintains a dedicated connection to one MCP server
- **Session Management**: Connections are session-based with unique `mcp-session-id`
- **Streaming Responses**: MCP servers can stream responses for real-time data

### DIAL Integration
**DIAL (Distributed AI Learning)** is an AI orchestration platform that your agent will use to:
- Send user messages and tool results to an LLM
- Receive AI-generated responses and tool calls
- Manage conversation flow

## 🏗️ Architecture

```
ai-dial-mcp-fundamentals/
├── agent/
│   ├── models/           
│   │   └── message.py        ✅ Complete
│   ├── app.py                🚧 TODO: implement logic
│   ├── prompts.py            🚧 TODO: write system prompt
│   ├── dial_client.py        🚧 TODO: implement logic
│   ├── mcp_client.py         🚧 TODO: implement logic
│   └── requirements.txt      
└── mcp_server/               
    ├── server.py             🚧 TODO: implement logic
    ├── user_client.py        ✅ Complete
    ├── models/
    │   └── user_info.py      ✅ Complete
    ├── Dockerfile            ✅ Complete
    └── requirements.txt
```

### Data Flow Diagram
![Architecture Flow](flow.png)

**Flow Explanation:**
1. User sends a query to the Agent
2. Agent connects to MCP Server to get available tools
3. Agent sends the query + tools to DIAL (LLM)
4. LLM decides which tools to call
5. Agent executes tools via MCP Server
6. MCP Server interacts with User Management Service
7. Results return to the Agent and then to the user

## 📋 Requirements

- **Python**: 3.11 or higher
- **Docker**: Latest version with Docker Compose
- **API Access**: DIAL API key with appropriate permissions
- **Network**: EPAM VPN connection for internal API access
- **Postman**: (Optional) For testing MCP server endpoints
- **Git**: For cloning and branch management

### Dependencies
Dependencies are listed in separate `requirements.txt` files:
- `agent/requirements.txt`: Agent dependencies (fastmcp, aiohttp, openai)
- `mcp_server/requirements.txt`: MCP server dependencies (fastmcp, requests)

## 🚀 Quick Start

```bash
# 1. Clone the repository
git clone https://github.com/GPretadoR/ai-dial-mcp-fundamentals.git
cd ai-dial-mcp-fundamentals

# 2. Set up environment
export DIAL_API_KEY="your-dial-api-key-here"

# 3. Start User Management Service
docker-compose up -d

# 4. Install dependencies
pip install -r mcp_server/requirements.txt
pip install -r agent/requirements.txt

# 5. Implement TODOs (see Tasks section below)

# 6. Run MCP server (in one terminal)
python mcp_server/server.py

# 7. Run agent (in another terminal)
python agent/app.py
```

## 🔧 Setup & Installation

### 1. Prerequisites Installation

#### Install Python 3.11+
```bash
# macOS (using Homebrew)
brew install python@3.11

# Verify installation
python3 --version  # Should show 3.11 or higher
```

#### Install Docker Desktop
Download and install from [docker.com](https://www.docker.com/products/docker-desktop)

```bash
# Verify installation
docker --version
docker-compose --version
```

### 2. Project Setup

#### Clone Repository
```bash
git clone https://github.com/GPretadoR/ai-dial-mcp-fundamentals.git
cd ai-dial-mcp-fundamentals
```

#### Set up Virtual Environment (Recommended)
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # On macOS/Linux
# or
.\venv\Scripts\activate   # On Windows
```

#### Install Dependencies
```bash
# Install MCP server dependencies
pip install -r mcp_server/requirements.txt

# Install agent dependencies
pip install -r agent/requirements.txt
```

### 3. Environment Configuration

#### Set DIAL API Key
```bash
# Export as environment variable
export DIAL_API_KEY="dial-your-api-key-here"

# Or create a .env file (if supported)
echo "DIAL_API_KEY=dial-your-api-key-here" > .env
```

**How to get DIAL API Key:**
1. Connect to EPAM VPN
2. Access DIAL platform (contact your team lead for URL)
3. Generate API key from your account settings

#### Verify EPAM VPN Connection
Ensure you're connected to EPAM VPN before running the agent, as it requires access to internal DIAL APIs.

### 4. Start User Management Service

```bash
# Start the mock user service
docker-compose up -d

# Verify it's running
curl http://localhost:8041/health

# View logs
docker-compose logs -f userservice
```

The service will:
- Run on `http://localhost:8041`
- Generate 1000 mock users automatically
- Provide REST API endpoints for CRUD operations

### 5. Verify Installation

```bash
# Check Python version
python3 --version

# Check installed packages
pip list | grep fastmcp
pip list | grep openai

# Check Docker containers
docker-compose ps

# Test User Service API
curl http://localhost:8041/users?page=1&limit=5
```

## ✍️ Tasks

> **💡 Tip**: If the tasks in the `main` branch are too challenging, switch to the `with-detailed-description` branch for more detailed guidance.

You need to implement the **Users Management Agent** that performs CRUD operations on the User Management Service via MCP tools.

---

### Create and run MCP server

**Goal**: Create an MCP server that exposes user management operations as MCP tools.

#### Steps:

1. **Start the User Service** (Optional if already running)
   ```bash
   docker-compose up -d
   ```
   This starts the mock User Management Service on `http://localhost:8041`

2. **Open server.py**
   ```bash
   # Edit this file
   mcp_server/server.py
   ```

3. **Implement all TODO sections**

   You need to implement:
   
   **a) FastMCP Server Initialization**
   ```python
   from mcp.server.fastmcp import FastMCP
   
   mcp = FastMCP(
       name="users-management-mcp-server",
       host="0.0.0.0",
       port=8005
   )
   
   user_client = UserClient()
   ```
   
   **b) Five MCP Tools** (use `@mcp.tool()` decorator):
   - `get_user_by_id(user_id: int) -> str` - Retrieve user by ID
   - `delete_user(user_id: int) -> str` - Delete a user
   - `search_user(request: UserSearchRequest) -> str` - Search users by criteria
   - `add_user(user: UserCreate) -> str` - Create a new user
   - `update_user(user_id: int, user: UserUpdate) -> str` - Update existing user
   
   Example tool implementation:
   ```python
   @mcp.tool()
   async def get_user_by_id(user_id: int) -> str:
       """Retrieves a user by their ID from the User Management Service.
       
       Args:
           user_id: The unique identifier of the user
           
       Returns:
           JSON string containing user information or error message
       """
       result = await user_client.get_user(user_id)
       return json.dumps(result)
   ```
   
   **c) MCP Resource** (use `@mcp.resource()` decorator):
   - `get_flow_diagram()` - Returns the flow diagram image
   
   ```python
   @mcp.resource(uri="users-management://flow-diagram", mime_type="image/png")
   async def get_flow_diagram() -> bytes:
       """Provides the architecture flow diagram as a resource."""
       diagram_path = Path(__file__).parent / "flow.png"
       return diagram_path.read_bytes()
   ```
   
   **d) MCP Prompts** (use `@mcp.prompt()` decorator):
   - Implement prompt methods that return predefined prompts
   - These can guide the LLM on how to use your tools

4. **Run the MCP server**
   ```bash
   python mcp_server/server.py
   ```
   
   **Expected Output:**
   ```
   INFO:     Started server process
   INFO:     Uvicorn running on http://0.0.0.0:8005
   ```

5. **Verify the server is running**
   ```bash
   # Test the health endpoint (if available)
   curl http://localhost:8005/health
   ```

---

### OPTIONAL: Work with MCP server in Postman

**Goal**: Test your MCP server manually using Postman to understand the MCP protocol.

#### Steps:

1. **Import the Postman collection**
   - Open Postman
   - Click **Import**
   - Select [mcp.postman_collection.json](mcp.postman_collection.json)

2. **Initialize MCP session** (Call: `init`)
   - Send POST request to `/mcp/init`
   - **Expected Response**: 
     - Status: 200 OK
     - Headers: Look for `mcp-session-id` (e.g., `abc123def456`)
   - **Save this session ID** for subsequent requests

3. **Send initialization notification** (Call: `init-notification`)
   - Send POST request with the `mcp-session-id` header
   - **Expected Response**: Status 202 Accepted

4. **Get available tools** (Call: `list tools`)
   - Include `mcp-session-id` header
   - **Expected Response**: 
     - Status: 200 OK
     - Streaming response with list of 5 tools (get_user_by_id, delete_user, etc.)

5. **Call a tool** (Call: `call tool`)
   - Example: Call `get_user_by_id` with `user_id: 1`
   - Include `mcp-session-id` header
   - **Expected Response**: Streaming response with user data

**Troubleshooting Postman:**
- If you get 401/403: Check your session ID is correct
- If stream doesn't display: Postman may show raw SSE format
- If connection fails: Verify MCP server is running on port 8005

---

### Create and run Agent

**Goal**: Build an AI agent that uses MCP tools to interact with users conversationally.

#### Steps:

1. **Implement MCP Client** ([agent/mcp_client.py](agent/mcp_client.py))
   
   Key methods to implement:
   ```python
   async def connect(self):
       """Establish SSE connection to MCP server"""
       
   async def get_tools(self):
       """Fetch available tools from MCP server"""
       
   async def call_tool(self, tool_name: str, arguments: dict):
       """Execute a tool on the MCP server"""
   ```

2. **Implement DIAL Client** ([agent/dial_client.py](agent/dial_client.py))
   
   Key methods to implement:
   ```python
   async def send_message(self, messages: List[Message], tools: List):
       """Send messages to DIAL LLM and get response with tool calls"""
       
   async def handle_tool_calls(self, tool_calls):
       """Process tool calls returned by LLM"""
   ```

3. **Write System Prompt** ([agent/prompts.py](agent/prompts.py))
   
   Create a prompt that instructs the LLM how to:
   - Use the available MCP tools
   - Handle user requests for CRUD operations
   - Format responses appropriately
   
   Example:
   ```python
   SYSTEM_PROMPT = """You are a helpful assistant that manages users in a User Management System.
   
   You have access to the following tools:
   - get_user_by_id: Retrieve a user by their ID
   - search_user: Search for users by name, email, or other criteria
   - add_user: Create a new user
   - update_user: Update an existing user's information
   - delete_user: Remove a user from the system
   
   When a user asks to perform an action, use the appropriate tool and provide clear feedback.
   """
   ```

4. **Implement Main Application** ([agent/app.py](agent/app.py))
   
   Implementation checklist:
   ```python
   async def main():
       # 1. Create MCP client and connect
       async with MCPClient(mcp_server_url="http://localhost:8005/mcp") as mcp_client:
           
           # 2. Get and print MCP resources
           resources = await mcp_client.get_resources()
           print("Available Resources:", resources)
           
           # 3. Get and print MCP tools
           tools = await mcp_client.get_tools()
           print("Available Tools:", [t['name'] for t in tools])
           
           # 4. Create DIAL client
           dial_client = DialClient(api_key=os.getenv("DIAL_API_KEY"))
           
           # 5. Initialize conversation with system prompt
           messages = [Message(role=Role.SYSTEM, content=SYSTEM_PROMPT)]
           
           # 6. Add MCP prompts to conversation
           prompts = await mcp_client.get_prompts()
           for prompt in prompts:
               messages.append(Message(role=Role.USER, content=prompt))
           
           # 7. Create console chat loop
           while True:
               user_input = input("You: ")
               if user_input.lower() in ["exit", "quit"]:
                   break
                   
               messages.append(Message(role=Role.USER, content=user_input))
               
               response = await dial_client.send_message(messages, tools)
               print(f"Assistant: {response}")
               
               messages.append(Message(role=Role.ASSISTANT, content=response))
   ```

5. **Run the application**
   ```bash
   # Make sure MCP server is running first
   python agent/app.py
   ```

6. **Test with queries**
   ```
   You: Get user with ID 1
   Assistant: [User info retrieved via MCP tool]
   
   You: Search for users named John
   Assistant: [Search results via MCP tool]
   
   You: Create a new user named Alice with email alice@example.com
   Assistant: [User created via MCP tool]
   ```

7. **Compare with remote MCP server**
   - Modify `mcp_server_url` to: `https://remote.mcpservers.org/fetch/mcp`
   - Run your agent and observe differences in the `init` step
   - Note: The `fetch` MCP server doesn't have resources or prompts
   - **Question to explore**: What tools does the fetch server provide?

---

### OPTIONAL: Support both (users-management and fetch) MCP servers

**Goal**: Enable your agent to use tools from multiple MCP servers simultaneously.

#### Challenge:
- MCP protocol enforces **1-to-1** connection between client and server
- You need to manage multiple MCP clients for multiple servers
- Tools from different servers should be aggregated for the LLM

#### Steps:

1. **Understand the limitation**
   - Each MCP client connects to ONE MCP server
   - You cannot connect one client to multiple servers

2. **Design a multi-server architecture**
   
   Hints:
   - Create multiple `MCPClient` instances
   - Each client connects to a different server
   - Aggregate tools from all clients before sending to DIAL
   - Track which tool belongs to which server

3. **Modify dial_client.py** (Main challenge area)
   ```python
   # Pseudocode example
   class DialClient:
       def __init__(self, mcp_clients: List[MCPClient]):
           self.mcp_clients = mcp_clients
           self.tool_registry = {}  # tool_name -> mcp_client
           
       async def aggregate_tools(self):
           all_tools = []
           for client in self.mcp_clients:
               tools = await client.get_tools()
               for tool in tools:
                   all_tools.append(tool)
                   self.tool_registry[tool['name']] = client
           return all_tools
           
       async def execute_tool(self, tool_name, args):
           client = self.tool_registry[tool_name]
           return await client.call_tool(tool_name, args)
   ```

4. **Implement the solution**
   - Connect to both `http://localhost:8005/mcp` and `https://remote.mcpservers.org/fetch/mcp`
   - Merge tool lists from both servers
   - Route tool calls to the appropriate MCP server

5. **Test the integration**
   ```
   You: Fetch information about Elon Musk from the web
   [Uses fetch MCP server]
   
   You: Now save Elon Musk as a user in our system
   [Uses users-management MCP server]
   ```

**Success Criteria:**
- Agent can fetch data from web (fetch server)
- Agent can save fetched data to User Service (users server)
- No conflicts between tool names from different servers

---

## 🧪 Testing & Validation

### Manual Testing Checklist

#### MCP Server Tests
- [ ] Server starts without errors on port 8005
- [ ] All 5 tools are registered (check server startup logs)
- [ ] Resources are accessible
- [ ] Postman collection works with valid session IDs

#### Agent Tests
```bash
# Test Case 1: Get User by ID
You: Get user with ID 1
Expected: User details returned in JSON format

# Test Case 2: Search Users
You: Find all users with first name John
Expected: List of matching users

# Test Case 3: Create User
You: Create a new user named Bob Smith with email bob@test.com
Expected: Confirmation with new user ID

# Test Case 4: Update User
You: Update user 1's email to newemail@test.com
Expected: Confirmation of update

# Test Case 5: Delete User
You: Delete user with ID 999
Expected: Confirmation of deletion or error if not found

# Test Case 6: Complex Query
You: Find all users and show me the first 3
Expected: List of 3 users

# Test Case 7: Error Handling
You: Get user with ID -1
Expected: Graceful error message
```

### Validation Commands

```bash
# Check MCP server is running
curl http://localhost:8005/health || echo "Server not responding"

# Check User Service is running
curl http://localhost:8041/users?page=1&limit=1

# Verify Docker containers
docker-compose ps | grep userservice

# Check Python packages installed
pip show fastmcp openai aiohttp

# Verify environment variables
echo $DIAL_API_KEY | grep -o "dial-.*"
```

### Success Criteria

✅ **MCP Server:**
- Server starts and listens on port 8005
- All tools are callable and return valid responses
- Resources are accessible
- Prompts are provided

✅ **Agent:**
- Successfully connects to MCP server
- Retrieves and displays available tools
- Can execute all CRUD operations via conversation
- Maintains conversation context across multiple turns
- Handles errors gracefully

✅ **Integration:**
- Agent + MCP Server + User Service work together
- Tool calls are properly executed
- Results are formatted and returned to user
- No crashes or unhandled exceptions

---

## 🔍 Troubleshooting

### Common Issues and Solutions

#### 1. MCP Server won't start

**Symptoms:**
- `Address already in use` error
- `ModuleNotFoundError: No module named 'fastmcp'`

**Solutions:**
```bash
# Check if port 8005 is in use
lsof -i :8005
# Kill the process if needed
kill -9 <PID>

# Reinstall dependencies
pip install -r mcp_server/requirements.txt

# Verify FastMCP version
pip show fastmcp  # Should be 2.10.1
```

#### 2. Agent can't connect to MCP server

**Symptoms:**
- `Connection refused` errors
- `Failed to connect to http://localhost:8005/mcp`

**Solutions:**
```bash
# Verify MCP server is running
curl http://localhost:8005/health

# Check firewall isn't blocking port 8005
# On macOS: System Preferences → Security & Privacy → Firewall

# Ensure you're using correct URL
# URL should be: http://localhost:8005/mcp (not just http://localhost:8005)
```

#### 3. DIAL API authentication fails

**Symptoms:**
- `401 Unauthorized` errors
- `Invalid API key` messages

**Solutions:**
```bash
# Verify API key is set
echo $DIAL_API_KEY

# Re-export with correct key
export DIAL_API_KEY="dial-your-actual-key"

# Ensure EPAM VPN is connected
# DIAL APIs require VPN access

# Check key format (should start with "dial-")
```

#### 4. User Service not responding

**Symptoms:**
- `Connection refused` to `localhost:8041`
- `curl: (7) Failed to connect`

**Solutions:**
```bash
# Check if container is running
docker-compose ps

# Restart the service
docker-compose down
docker-compose up -d

# Check container logs
docker-compose logs userservice

# Verify port mapping
docker-compose ps | grep 8041
```

#### 5. Tools not appearing in agent

**Symptoms:**
- Agent shows empty tools list
- `No tools available` message

**Solutions:**
```bash
# Verify MCP server implemented @mcp.tool() decorators
# Check server.py has all 5 tool functions

# Ensure MCP client's get_tools() method is implemented
# Check agent/mcp_client.py

# Test tools endpoint directly
curl http://localhost:8005/mcp/tools
```

#### 6. Postman session issues

**Symptoms:**
- `mcp-session-id` not in response headers
- 401/403 errors on subsequent requests

**Solutions:**
- Ensure you're calling `/mcp/init` first
- Check response headers (not body) for session ID
- Copy entire session ID value
- Add `mcp-session-id` to headers of all subsequent requests
- Session IDs may expire - reinitialize if needed

#### 7. Module import errors

**Symptoms:**
```
ModuleNotFoundError: No module named 'agent'
ImportError: attempted relative import with no known parent package
```

**Solutions:**
```bash
# Run from project root directory
cd /path/to/ai-dial-mcp-fundamentals

# Use module syntax
python -m agent.app  # instead of python agent/app.py

# Or add project root to PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
python agent/app.py
```

#### 8. Docker Compose errors

**Symptoms:**
- `service 'userservice' failed to build`
- `network not found`

**Solutions:**
```bash
# Remove old containers and networks
docker-compose down --volumes --remove-orphans

# Pull latest image
docker pull khshanovskyi/mockuserservice:latest

# Rebuild
docker-compose up -d --build

# Check Docker daemon is running
docker info
```

### Debug Mode

Enable debug logging for more detailed error messages:

```python
# In mcp_server/server.py
import logging
logging.basicConfig(level=logging.DEBUG)

# In agent/app.py
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Getting Help

If issues persist:
1. Check the `with-detailed-description` branch for additional guidance
2. Review server and agent logs for stack traces
3. Verify all TODO sections are implemented
4. Compare your implementation with FastMCP documentation
5. Contact your team lead or instructor

---

## 🌿 Branch Information

This repository has two main branches:

### `main` Branch (Current)
- **Difficulty**: Intermediate
- **Description**: Contains TODO markers with minimal guidance
- **Best For**: Developers familiar with Python, async programming, and API concepts
- **Files**: Minimal implementation hints in code comments

### `with-detailed-description` Branch
- **Difficulty**: Beginner-friendly
- **Description**: Contains detailed TODO descriptions with code examples
- **Best For**: Developers new to MCP, FastMCP, or async Python
- **Files**: Extensive comments, code snippets, and step-by-step guidance

### Switching Branches

```bash
# View current branch
git branch

# Switch to detailed description branch
git checkout with-detailed-description

# Switch back to main
git checkout main
```

**Recommendation**: Start with `with-detailed-description` if you're new to MCP or struggling with implementation. Switch to `main` once you understand the concepts.

---

## 📚 Additional Resources

### MCP Protocol
- [MCP Specification](https://spec.modelcontextprotocol.io/)
- [MCP GitHub Repository](https://github.com/modelcontextprotocol)

### FastMCP Framework
- [FastMCP Documentation](https://gofastmcp.com/)
- [FastMCP Tools Guide](https://gofastmcp.com/servers/tools)
- [FastMCP Resources Guide](https://gofastmcp.com/servers/resources)
- [FastMCP Prompts Guide](https://gofastmcp.com/servers/prompts)

### Python Async Programming
- [Python asyncio Documentation](https://docs.python.org/3/library/asyncio.html)
- [Real Python: Async IO](https://realpython.com/async-io-python/)

### DIAL Platform
- Contact your team lead for internal DIAL documentation
- DIAL API documentation (requires EPAM VPN)

---

<img src="dialx-banner.png">
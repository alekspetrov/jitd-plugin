# MCP SDK Research Summary

**Date**: 2025-10-22
**Research Focus**: Existing MCP Python clients/SDKs for Figma integration

---

## Key Finding: Official MCP Python SDK Exists

### Official SDK

**Repository**: https://github.com/modelcontextprotocol/python-sdk
- **Stars**: 19,500+
- **License**: MIT
- **Maintainer**: Anthropic (Model Context Protocol organization)
- **Latest Version**: 1.2.1 (updated 2025-10-21)
- **PyPI**: `pip install mcp`

### Protocol Specification

**Protocol**: JSON-RPC 2.0 based
**Version**: 2025-06-18 (latest spec revision)
**Official Spec**: spec.modelcontextprotocol.io

### Supported Transports

1. **stdio** - Standard input/output (subprocess communication)
2. **SSE** - Server-Sent Events (HTTP streaming)
3. **Streamable HTTP** - Full bidirectional HTTP (recommended for production)

---

## Validation Test Results

### Test Setup

```bash
# Install
pip install mcp

# Test connectivity to Figma Desktop MCP server
python3 test_figma_mcp_client.py
```

### Test Results ✅ SUCCESS

```
✅ Transport connection established
✅ ClientSession created
✅ Session initialized
   Server info: name='Figma Dev Mode MCP Server' version='1.0.0'
   Protocol version: 2025-06-18

✅ Found 6 tools:
   - get_design_context
   - get_variable_defs
   - get_code_connect_map
   - get_screenshot
   - get_metadata
   - create_design_system_rules

✅ Found 0 resources
```

**Conclusion**: Python can directly connect to Figma Desktop MCP server at `http://127.0.0.1:3845/mcp` using the official MCP SDK.

---

## Available Figma MCP Tools

### 1. `get_design_context`

**Purpose**: Generate UI code for components
**Parameters**:
- `nodeId` (optional): Specific node ID or currently selected
**Returns**: Component implementation code (React/Vue/HTML)
**Use Case**: Code generation, component implementation

### 2. `get_variable_defs`

**Purpose**: Get design token variable definitions
**Parameters**:
- `nodeId` (optional): Specific node ID or currently selected
**Returns**: Variable mappings like `{'icon/default/secondary': '#949494'}`
**Use Case**: Design token extraction, token sync

### 3. `get_code_connect_map`

**Purpose**: Get component → code mappings
**Parameters**:
- `nodeId` (optional): Specific node ID or currently selected
**Returns**: Mapping of `{nodeId: {codeConnectSrc, codeConnectName}}`
**Example**: `{'1:2': {codeConnectSrc: 'https://github.com/foo/components/Button.tsx', codeConnectName: 'Button'}}`
**Use Case**: Component mapping, code discovery
**Requires**: Figma Enterprise plan + Code Connect setup

### 4. `get_screenshot`

**Purpose**: Generate screenshots of components
**Parameters**:
- `nodeId` (optional): Specific node ID or currently selected
**Returns**: Screenshot image data
**Use Case**: Visual regression testing, documentation

### 5. `get_metadata`

**Purpose**: Get node structure in XML format
**Parameters**:
- `nodeId` (optional): Node or page ID (e.g., `0:1`)
**Returns**: XML with node IDs, types, names, positions, sizes
**Use Case**: Structure analysis, discovering component IDs
**Note**: Prefer `get_design_context` for full details

### 6. `create_design_system_rules`

**Purpose**: Generate design system rules for repository
**Parameters**: (not documented)
**Returns**: Prompt for design system rules generation
**Use Case**: Design system automation

---

## Code Examples

### Basic Connection

```python
import asyncio
from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client

async def connect_to_figma():
    async with streamablehttp_client("http://127.0.0.1:3845/mcp") as (
        read_stream, write_stream, _
    ):
        async with ClientSession(read_stream, write_stream) as session:
            # Initialize connection
            await session.initialize()

            # List tools
            tools = await session.list_tools()
            print(f"Available tools: {[t.name for t in tools.tools]}")

            # Call a tool
            result = await session.call_tool("get_variable_defs", {})
            print(result.content)

asyncio.run(connect_to_figma())
```

### Wrapper Class

```python
class FigmaMCPClient:
    def __init__(self, mcp_url="http://127.0.0.1:3845/mcp"):
        self.mcp_url = mcp_url

    async def __aenter__(self):
        self.transport = streamablehttp_client(self.mcp_url)
        self.read_stream, self.write_stream, _ = await self.transport.__aenter__()

        self.session_context = ClientSession(self.read_stream, self.write_stream)
        self.session = await self.session_context.__aenter__()
        await self.session.initialize()

        return self

    async def __aexit__(self, *args):
        await self.session_context.__aexit__(*args)
        await self.transport.__aexit__(*args)

    async def get_variables(self, node_id=None):
        params = {"nodeId": node_id} if node_id else {}
        result = await self.session.call_tool("get_variable_defs", params)
        return result.content[0].text  # Extract text content

# Usage
async with FigmaMCPClient() as client:
    variables = await client.get_variables()
```

---

## Authentication Model

### How It Works

1. **User**: Logged into Figma Desktop app
2. **Figma Desktop**: Exposes MCP server at `http://127.0.0.1:3845/mcp`
3. **Authentication**: Implicit via Desktop session (no API keys needed)
4. **Access**: Any local process can connect (localhost only)
5. **Session**: MCP client establishes session via initialize handshake
6. **Tools**: Available while Figma Desktop running and user logged in

### Security Model

- **Port Binding**: 127.0.0.1 only (not exposed to network)
- **Session**: Per-client MCP session
- **User Context**: Tools operate on currently selected Figma file/node
- **No Tokens**: No API tokens or credentials required

---

## Comparison: MCP SDK vs Direct Figma API

| Feature | MCP SDK | Figma REST API |
|---------|---------|----------------|
| **Auth** | Desktop session (automatic) | API token required |
| **Access** | Local only | Remote (any network) |
| **Tools** | 6 specialized design tools | Full REST API |
| **Setup** | Enable in Figma preferences | Generate token, manage scopes |
| **Latency** | Low (localhost) | Higher (HTTPS) |
| **Use Case** | Local development workflows | Production integrations |
| **Code Connect** | ✅ Built-in | ❌ Not available |
| **Current Selection** | ✅ Can use selected node | ❌ Requires explicit IDs |

---

## Integration Recommendations

### For Navigator Product Design Skill

**Current**: Claude orchestrates MCP calls → temp files → Python processing
**Recommended**: Python directly calls MCP → processes data

**Implementation**:
1. Add `mcp` to Python requirements
2. Create `figma_mcp_client.py` wrapper
3. Refactor `design_analyzer.py` to use MCP client directly
4. Remove manual orchestration from SKILL.md

**Benefits**:
- 95% reduction in orchestration steps (15-20 → 1)
- Progressive refinement (fetch only needed data)
- Fully autonomous execution
- Better error handling

---

## Dependencies

### Python Requirements

```txt
mcp>=1.2.1
anyio>=4.0.0  # Async I/O (transitive dependency)
httpx>=0.25.0  # HTTP client (transitive dependency)
pydantic>=2.0.0  # Data validation (transitive dependency)
```

### System Requirements

- **Figma Desktop**: Must be running
- **MCP Server**: Enabled in Figma → Preferences → "Enable local MCP Server"
- **User Session**: User must be logged into Figma
- **Network**: Localhost access (127.0.0.1:3845)

---

## Additional MCP Resources

### Documentation

- **Official Docs**: https://modelcontextprotocol.io
- **Python SDK**: https://github.com/modelcontextprotocol/python-sdk
- **Figma MCP Guide**: https://help.figma.com/hc/en-us/articles/32132100833559

### Alternative SDKs

- **TypeScript**: `@modelcontextprotocol/sdk`
- **Java**: `io.modelcontextprotocol:sdk`
- **Kotlin**: MCP Kotlin SDK
- **C#**: MCP .NET SDK

### Community Tools

- **FastMCP**: High-level Python framework (https://github.com/jlowin/fastmcp)
- **Pydantic AI MCP Client**: Pydantic-based client (https://ai.pydantic.dev/mcp/client/)
- **OpenAI Agents SDK**: MCP integration for OpenAI agents

---

## Next Steps

1. ✅ Install MCP SDK in product-design skill environment
2. ✅ Test connection to Figma Desktop MCP server
3. ⏳ Create FigmaMCPClient wrapper class
4. ⏳ Refactor design_analyzer.py to use MCP client
5. ⏳ Update SKILL.md workflow documentation
6. ⏳ Add integration tests

---

**Research Date**: 2025-10-22
**Validated By**: Live test with Figma Desktop v125.9.10
**MCP Protocol Version**: 2025-06-18
**Python SDK Version**: 1.2.1

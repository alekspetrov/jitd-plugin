#!/usr/bin/env python3
"""
Figma MCP Client - Direct Python interface to Figma Desktop MCP server.

This module provides a simple async interface to Figma's Model Context Protocol
server running locally at http://127.0.0.1:3845/mcp

Usage:
    async with FigmaMCPClient() as client:
        # Get design tokens
        tokens = await client.get_variable_defs()

        # Get component metadata
        metadata = await client.get_metadata(node_id="1:23")

        # Get code mappings
        mappings = await client.get_code_connect_map()

Requirements:
    - Figma Desktop app must be running
    - MCP server enabled in Figma Preferences
    - User logged into Figma
    - pip install mcp
"""

import json
import logging
from typing import Optional, Dict, Any, List

try:
    from mcp import ClientSession
    from mcp.client.streamable_http import streamablehttp_client
except ImportError as e:
    raise ImportError(
        "MCP SDK not installed. Install with: pip install mcp"
    ) from e


logger = logging.getLogger(__name__)


class FigmaMCPError(Exception):
    """Base exception for Figma MCP client errors."""
    pass


class FigmaNotRunningError(FigmaMCPError):
    """Raised when Figma Desktop is not running or MCP server not enabled."""
    pass


class FigmaMCPClient:
    """
    Async client for Figma Desktop MCP server.

    Provides direct access to Figma's design data through the Model Context Protocol.
    Use as async context manager to ensure proper connection lifecycle.

    Example:
        async with FigmaMCPClient() as client:
            variables = await client.get_variable_defs()
            print(f"Found {len(variables)} design tokens")
    """

    def __init__(self, mcp_url: str = "http://127.0.0.1:3845/mcp"):
        """
        Initialize Figma MCP client.

        Args:
            mcp_url: URL of Figma Desktop MCP server (default: http://127.0.0.1:3845/mcp)
        """
        self.mcp_url = mcp_url
        self.session = None
        self.transport = None
        self.session_context = None

    async def __aenter__(self):
        """Async context manager entry - establishes MCP connection."""
        try:
            # Connect to Figma MCP server
            self.transport = streamablehttp_client(self.mcp_url)
            self.read_stream, self.write_stream, _ = await self.transport.__aenter__()

            # Create MCP session
            self.session_context = ClientSession(self.read_stream, self.write_stream)
            self.session = await self.session_context.__aenter__()

            # Initialize MCP protocol
            init_result = await self.session.initialize()
            logger.info(
                f"Connected to {init_result.serverInfo.name} "
                f"v{init_result.serverInfo.version}"
            )

            return self

        except Exception as e:
            logger.error(f"Failed to connect to Figma MCP server: {e}")
            raise FigmaNotRunningError(
                "Could not connect to Figma Desktop MCP server. "
                "Please ensure:\n"
                "  1. Figma Desktop app is running\n"
                "  2. MCP server is enabled in Figma → Preferences\n"
                "  3. You are logged into Figma\n"
                f"Error: {e}"
            ) from e

    async def __aexit__(self, *args):
        """Async context manager exit - closes MCP connection."""
        try:
            if self.session_context:
                await self.session_context.__aexit__(*args)
            if self.transport:
                await self.transport.__aexit__(*args)
            logger.info("Disconnected from Figma MCP server")
        except Exception as e:
            logger.warning(f"Error during disconnect: {e}")

    async def _call_tool(self, tool_name: str, params: Optional[Dict[str, Any]] = None) -> Any:
        """
        Internal method to call MCP tool and extract content.

        Args:
            tool_name: Name of the MCP tool to call
            params: Tool parameters

        Returns:
            Tool response content (parsed as JSON if possible)
        """
        if not self.session:
            raise FigmaMCPError("Client not connected. Use 'async with FigmaMCPClient()'")

        try:
            result = await self.session.call_tool(tool_name, params or {})

            # Extract content from MCP response
            if result.content and len(result.content) > 0:
                content_item = result.content[0]

                # Handle different content types
                if hasattr(content_item, 'text'):
                    # Text content (most common)
                    content = content_item.text

                    # Try to parse as JSON
                    try:
                        return json.loads(content)
                    except (json.JSONDecodeError, TypeError):
                        # Return raw text if not JSON
                        return content

                elif hasattr(content_item, 'data'):
                    # Image or binary content
                    return content_item.data

                else:
                    # Unknown content type - return as-is
                    return content_item

            return None

        except Exception as e:
            logger.error(f"Error calling {tool_name}: {e}")
            raise FigmaMCPError(f"Failed to call {tool_name}: {e}") from e

    async def get_metadata(self, node_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Get metadata for a node or page in XML format.

        Includes node IDs, layer types, names, positions, and sizes.
        Use this to discover component structure before fetching full details.

        Args:
            node_id: Specific node or page ID (e.g., "1:23" or "0:1")
                    If None, uses currently selected node in Figma

        Returns:
            Metadata dictionary with node structure

        Example:
            metadata = await client.get_metadata(node_id="0:1")
            # Parse to find component node IDs
        """
        params = {"nodeId": node_id} if node_id else {}
        return await self._call_tool("get_metadata", params)

    async def get_variable_defs(self, node_id: Optional[str] = None) -> Dict[str, str]:
        """
        Get design token variable definitions.

        Returns mapping of variable names to values.

        Args:
            node_id: Specific node ID (if None, uses currently selected)

        Returns:
            Dictionary mapping variable names to values
            Example: {'icon/default/secondary': '#949494', 'spacing/md': '16px'}

        Example:
            tokens = await client.get_variable_defs()
            for name, value in tokens.items():
                print(f"{name}: {value}")
        """
        params = {"nodeId": node_id} if node_id else {}
        return await self._call_tool("get_variable_defs", params)

    async def get_code_connect_map(self, node_id: Optional[str] = None) -> Dict[str, Dict[str, str]]:
        """
        Get mapping of Figma components to code components.

        Requires Figma Enterprise plan with Code Connect configured.

        Args:
            node_id: Specific node ID (if None, uses currently selected)

        Returns:
            Dictionary mapping node IDs to code locations
            Example: {
                '1:2': {
                    'codeConnectSrc': 'https://github.com/foo/components/Button.tsx',
                    'codeConnectName': 'Button'
                }
            }

        Example:
            mappings = await client.get_code_connect_map()
            for node_id, mapping in mappings.items():
                print(f"{node_id} → {mapping['codeConnectName']}")
        """
        params = {"nodeId": node_id} if node_id else {}
        return await self._call_tool("get_code_connect_map", params)

    async def get_design_context(self, node_id: Optional[str] = None) -> str:
        """
        Generate UI code for a component.

        Returns React/Vue/HTML implementation code for the selected component.
        Use sparingly - can return large responses (50-100k tokens).

        Args:
            node_id: Specific node ID (if None, uses currently selected)

        Returns:
            UI code as string (React/Vue/HTML)

        Example:
            code = await client.get_design_context(node_id="1:23")
            # Returns React component code
        """
        params = {"nodeId": node_id} if node_id else {}
        return await self._call_tool("get_design_context", params)

    async def get_screenshot(self, node_id: Optional[str] = None) -> str:
        """
        Generate screenshot for a component.

        Args:
            node_id: Specific node ID (if None, uses currently selected)

        Returns:
            Screenshot image data (format depends on Figma response)

        Example:
            screenshot = await client.get_screenshot(node_id="1:23")
            # Save or process screenshot data
        """
        params = {"nodeId": node_id} if node_id else {}
        return await self._call_tool("get_screenshot", params)

    async def create_design_system_rules(self) -> str:
        """
        Generate design system rules for the repository.

        Returns:
            Prompt for design system rules generation

        Example:
            rules = await client.create_design_system_rules()
        """
        return await self._call_tool("create_design_system_rules")

    async def list_available_tools(self) -> List[str]:
        """
        List all available MCP tools.

        Useful for debugging or discovering what Figma MCP supports.

        Returns:
            List of tool names

        Example:
            tools = await client.list_available_tools()
            print(f"Available: {', '.join(tools)}")
        """
        if not self.session:
            raise FigmaMCPError("Client not connected")

        result = await self.session.list_tools()
        return [tool.name for tool in result.tools]


# Convenience function for simple use cases
async def get_figma_variables() -> Dict[str, str]:
    """
    Quick helper to fetch Figma design tokens.

    Returns:
        Dictionary of variable name → value mappings

    Example:
        tokens = await get_figma_variables()
    """
    async with FigmaMCPClient() as client:
        return await client.get_variable_defs()


async def get_figma_metadata(node_id: Optional[str] = None) -> Dict[str, Any]:
    """
    Quick helper to fetch Figma node metadata.

    Args:
        node_id: Specific node ID (if None, uses currently selected)

    Returns:
        Metadata dictionary

    Example:
        metadata = await get_figma_metadata(node_id="0:1")
    """
    async with FigmaMCPClient() as client:
        return await client.get_metadata(node_id)

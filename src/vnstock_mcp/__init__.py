"""VNStock MCP Server - Vietnamese Stock Market Data for Claude Desktop."""

__author__ = "gahoccode"

from vnstock_mcp.version import get_distribution_version

__version__ = get_distribution_version()

from .server import main

__all__ = ["main"]

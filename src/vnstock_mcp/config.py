"""Configuration constants for VNStock MCP Server."""

import os

# Service metadata
SERVICE_NAME = "vnstock"
VERSION = "0.2.0"

# Transport configuration
# If PORT env var is set (e.g., by Render), use HTTP transport
# Otherwise, default to STDIO transport for local usage (uvx)
PORT = int(os.environ.get("PORT", 8001))
USE_HTTP = "PORT" in os.environ

# Valid parameter values
VALID_LANGUAGES = frozenset(["en", "vi"])
VALID_INFO_TYPES = frozenset([
    "overview",
    "shareholders",
    "officers",
    "subsidiaries",
    "events",
    "news",
    "reports",
    "ratio_summary",
    "trading_stats",
])
VALID_FUND_TYPES = frozenset(["", "BALANCED", "BOND", "STOCK"])
VALID_OFFICER_FILTERS = frozenset(["working", "resigned", "all"])
VALID_SUBSIDIARY_FILTERS = frozenset(["all", "subsidiary"])
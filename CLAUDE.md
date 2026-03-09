# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**VNStock MCP Server** is an unofficial MCP (Model Context Protocol) server that provides Vietnamese stock market financial data integration through FastMCP 2.0. The project enables natural language interaction with Vietnamese financial data through Claude Desktop.

## Development Commands

### Setup and Installation
```bash
# Install dependencies (recommended)
uv sync

# Alternative installation
pip install -e .

# Install development dependencies
uv sync --dev
```

### Running the Server
```bash
# Recommended with uv
uv run python server.py



## Architecture Overview

### Core Structure
- **`server.py`** - Single main file containing all MCP server tools
- **`pyproject.toml`** - Modern project configuration with uv dependency management
- **`tests/`** - Test suite with pytest configuration

### Key Components
The server is organized into 3 main tool categories (11 tools total):

1. **Financial Analysis Tools (4)** - Income statements, balance sheets, cash flows, ratios
2. **Company Information Tools (1 multi-type)** - Company overview, shareholders, officers, subsidiaries, events
3. **Fund Management Tools (6)** - Mutual fund listings, NAV reports, holdings, allocations

### Data Sources
- **VCI** - Primary source for financials, company info
- **FMarket** - Fund data

## Technical Implementation

### Async Architecture
- All tools use `async def` with proper event loop management
- Non-blocking operations via `loop.run_in_executor()`
- Consistent JSON string return format for all data
- Comprehensive error handling with user-friendly messages

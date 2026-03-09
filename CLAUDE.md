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
uv run python src/vnstock_mcp/server.py
```

### Docker Commands

```bash
# Build Docker image
docker build -t vnstock-mcp:latest .

# Run standalone container (HTTP mode)
docker compose up

# Run with Docker MCP Gateway
docker compose -f docker-compose.gateway.yml up

# Run in STDIO mode (no PORT = STDIO transport)
docker run -i --rm vnstock-mcp:latest

# Export requirements.txt from pyproject.toml (after dependency changes)
uv export --format requirements-txt --no-emit-project > requirements.txt
```

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

# Docker

The wordcloud package needs gcc to compile a C extension so install build dependencies in the builder stage

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

## Registry Management

- The registry tracks installed servers

**Manage through CLI**

```bash
# List registered servers
docker mcp server list

# Add to registry
docker mcp server add my-server

# Remove from registry
docker mcp server remove my-server
```

## macOS Installation

### Step 1: Install Docker Desktop

1. Download Docker Desktop for Mac:
   - **Apple Silicon (M1/M2/M3)**: [Download here](https://desktop.docker.com/mac/main/arm64/Docker.dmg)
   - **Intel Mac**: [Download here](https://desktop.docker.com/mac/main/amd64/Docker.dmg)

2. Open the downloaded `.dmg` file
3. Drag Docker to Applications folder
4. Launch Docker from Applications
5. Accept the service agreement

### Step 2: Enable MCP Toolkit

1. Click Docker icon in menu bar
2. Open **Preferences** → **Beta Features**
3. Enable **"Docker MCP Toolkit"**
4. Click **Apply & Restart**

### Step 3: Install Claude Desktop

1. Download from [claude.ai/download](https://claude.ai/download)
2. Open the `.dmg` file
3. Drag Claude to Applications
4. Launch Claude and sign in

### Step 4: Configure MCP Connection

```bash
# Create MCP directories
mkdir -p ~/.docker/mcp/catalogs

# Edit Claude configuration
nano ~/Library/Application\ Support/Claude/claude_desktop_config.json
```

[For other OS, check out theNetworkChuck/docker-mcp-tutorial](https://raw.githubusercontent.com/theNetworkChuck/docker-mcp-tutorial/refs/heads/main/docs/installation.md)

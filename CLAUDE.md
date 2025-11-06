# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**VNStock MCP Server** is an unofficial MCP (Model Context Protocol) server that provides comprehensive Vietnamese stock market data integration through FastMCP 2.0. The project enables natural language interaction with Vietnamese financial data through Claude Desktop.

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
The server is organized into 6 main tool categories:

1. **Market Data Tools** - Stock history, forex, crypto, indices data
2. **Financial Analysis Tools** - Income statements, balance sheets, cash flows, ratios, dividends
3. **Company Information Tools** - Company overview, shareholders, officers, subsidiaries, events
4. **Precious Metals Tools** - SJC and BTMC gold prices
5. **Exchange Rate Tools** - Vietcombank exchange rates
6. **Fund Management Tools** - Mutual fund listings, NAV reports, holdings, allocations

### Data Sources
- **VCI** - Primary source for stocks, financials, company info
- **MSN** - Forex, crypto, international indices
- **TCBS** - Dividend data
- **Direct APIs** - Gold prices (SJC, BTMC) and exchange rates (VCB)

## Technical Implementation

### Async Architecture
- All tools use `async def` with proper event loop management
- Non-blocking operations via `loop.run_in_executor()`
- Consistent JSON string return format for all data
- Comprehensive error handling with user-friendly messages
- you don't use uv to set your service's 
Python version for deployment on Render
- you can generate a requirements.txt from your Astral uv pyproject.toml using uv’s export feature. The recommended command is: uv export --format requirements-txt > requirements.txt
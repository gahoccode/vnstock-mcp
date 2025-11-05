# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Vietnamese Stock Market MCP (Model Context Protocol) Server built with FastMCP 2.0. It provides 20 async tools for accessing Vietnamese financial data including stock prices, financial statements, portfolio optimization, and mutual fund information through the vnstock library.

## Development Environment

This project uses **uv** for modern Python dependency management.

### Essential Commands

```bash
# Install dependencies
uv sync                     # Production dependencies only
uv sync --group dev        # Include development tools

# Run the MCP server
uv run python server.py

# Development tools
uv run --group dev python -m pytest tests/     # Run tests
uv run --group dev python -m black .           # Format code
uv run --group dev ruff check .                # Lint code
uv run --group dev python -m mypy .            # Type checking

# Add dependencies
uv add package-name          # Production dependency
uv add --dev package-name    # Development dependency
```

## Architecture

### Core Components

- **FastMCP 2.0 Server**: Async MCP server providing tools via stdio protocol
- **vnstock Library**: Primary data source for Vietnamese market data
- **pyportfolioopt**: Portfolio optimization and calculations
- **Async/Await Pattern**: All tools use `asyncio.run_in_executor()` for non-blocking I/O

### Tool Categories

1. **Market Data (4 tools)**: Stock, forex, crypto, index historical data
2. **Financial Analysis (6 tools)**: Income statements, balance sheets, ratios, etc.
3. **Portfolio Optimization (3 tools)**: Mean-variance optimization, efficient frontier
4. **Company Information (4 tools)**: Overview, dividends, gold prices, exchange rates
5. **Mutual Funds (6 tools)**: Fund listings, NAV reports, holdings, allocations

### Key Patterns

All tools follow this async pattern:
```python
@mcp.tool()
async def tool_function(params) -> str:
    try:
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(None, lambda: blocking_operation())
        return result.to_json(orient="records", date_format="iso", indent=2)
    except Exception as e:
        return f"Error: {str(e)}"
```

## Important Implementation Details

### Data Sources
- **VCI source**: Primary for Vietnamese stocks and indices
- **TCBS source**: Required for dividend data only
- **MSN source**: Used for forex, crypto, international indices

### Critical Dependencies
- **FastMCP 2.0**: Requires Python 3.10+
- **vnstock**: Vietnamese market data API wrapper
- **pyportfolioopt**: Portfolio optimization (import as `pypfopt` in code)

### Configuration Files
- **pyproject.toml**: Single source of truth for dependencies and tool config
- **uv.lock**: Deterministic dependency lock file
- **.gitignore**: Excludes `.venv/`, `.uv-cache/`, Python cache files

### Error Handling
All tools return JSON-formatted data on success and descriptive error strings on failure. No exceptions are propagated to the MCP client.

## Testing

- **pytest**: Test framework with async support (`pytest-asyncio`)
- **conftest.py**: Provides sample symbols and date fixtures
- **Test structure**: Tests located in `tests/` directory
- **Run specific test**: `uv run --group dev python -m pytest tests/test_file.py::test_function`

## Common Development Tasks

### Adding New Tools
1. Define async function with `@mcp.tool()` decorator
2. Use `asyncio.run_in_executor()` for blocking operations
3. Return JSON string or error message
4. Add comprehensive docstring with parameter descriptions

### Dependency Management
- All dependencies managed through `pyproject.toml`
- Development tools in `[dependency-groups.dev]` section
- Use `uv add` rather than manual editing

### Code Quality
- **Black**: Code formatting (line length 88)
- **Ruff**: Linting and additional formatting
- **MyPy**: Type checking (Python 3.10+ baseline)

## Environment Variables

Copy `.env.example` to `.env` and configure:
- `ANTHROPIC_API_KEY`: For LLM integration (optional)

## Project Notes

- **Single file architecture**: All 20 tools in `server.py` (1197 lines)
- **No package structure**: Script-based project, not installable as package
- **uv-managed**: Modern Python workflow, no manual venv activation needed
- **FastMCP 2.0**: Latest async MCP server implementation
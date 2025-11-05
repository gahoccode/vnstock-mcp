# VNStock MCP Client

A powerful CLI client for interacting with Vietnamese Stock Market data through your MCP server, with integrated LLM capabilities for natural language queries.

## Features

- 🚀 **Direct MCP Integration**: Connect to your vnstock MCP server via stdio
- 🤖 **LLM-Powered**: Natural language processing with Anthropic Claude
- 💬 **Interactive CLI**: Rich terminal interface with auto-completion and history
- 📊 **Beautiful Output**: Formatted tables, charts, and data visualization
- 🔧 **Tool Management**: Automatic tool discovery and validation
- 🎯 **Smart Parsing**: Vietnamese stock symbol and date format support
- ⚡ **Error Handling**: Robust error recovery and user-friendly messages

## Quick Start

### 1. Installation

```bash
# Clone or navigate to your vnstock-mcp directory
cd vnstock-mcp

# Install uv if you don't have it
pip install uv

# Install dependencies with uv (recommended)
uv sync

# Or install with pip (legacy method)
pip install -e .
```

### 2. Setup Environment

```bash
# Copy environment template
cp .env.example .env

# Edit .env with your API key and server path
nano .env
```

Add your Anthropic API key (optional but recommended):
```bash
ANTHROPIC_API_KEY=your_anthropic_api_key_here
SERVER_PATH=/path/to/your/server.py
```

### 3. Run the Server

```bash
# Start the MCP server (recommended with uv)
uv run python server.py

# Or with python directly
python server.py
```

### 4. Run the Client

```bash
# Basic usage (looks for server.py in current directory)
uv run python client.py

# Specify server path
uv run python client.py --server-path /path/to/server.py

# Enable debug logging
uv run python client.py --debug
```

## Usage Examples

### Natural Language Queries (with LLM)

When you provide an `ANTHROPIC_API_KEY`, you can ask questions in natural language:

```
> What's the current price of VNM stock?
> Show me FPT's financial statements for 2024
> Optimize a portfolio with VNM, FPT, and HPG
> Get the latest SJC gold price
> What are HPG's key financial ratios?
> Show me dividend history for ACB stock
```

### Direct Tool Commands

List all available tools:
```
> tools
```

Call a specific tool:
```
> call get_stock_history --symbol VNM --start_date 2024-01-01 --end_date 2024-12-31
```

### Built-in Commands

- `help` - Show available commands and usage
- `tools` - List all available MCP tools
- `clear` - Clear the screen
- `exit` or `quit` - Exit the client
- `llm <query>` - Force LLM processing of a query

## Available Tools

The client automatically discovers all tools from your MCP server. Based on your `server.py`, these include:

### Stock Market Data
- `get_stock_history` - Historical stock prices
- `get_forex_history` - Foreign exchange rates
- `get_crypto_history` - Cryptocurrency prices
- `get_index_history` - Market indices data

### Financial Analysis
- `get_income_statement` - Company income statements
- `get_balance_sheet` - Balance sheet data
- `get_cash_flow` - Cash flow statements
- `get_financial_ratios` - Financial ratios and metrics
- `get_dividend_history` - Dividend payment history

### Company Information
- `get_company_info` - Company overview and details
- `get_sjc_gold_price` - SJC gold prices
- `get_btmc_gold_price` - BTMC gold prices
- `get_vcb_exchange_rate` - Vietcombank exchange rates

### Portfolio Optimization
- `calculate_returns` - Portfolio return calculations
- `optimize_portfolio` - Mean-variance optimization
- `full_portfolio_optimization` - Comprehensive optimization strategies

### Mutual Funds
- `get_fund_listing` - List available mutual funds
- `search_funds` - Search for specific funds
- `get_fund_nav_report` - Historical NAV data
- `get_fund_top_holdings` - Fund top holdings
- `get_fund_industry_allocation` - Industry allocation
- `get_fund_asset_allocation` - Asset allocation

## Configuration

The client can be configured via `config.toml`:

```toml
[server]
path = "./server.py"
timeout = 30

[display]
table_style = "grid"
max_rows = 1000

[llm]
model = "claude-3-5-haiku-20241022"
max_tokens = 1000

[defaults]
start_date = "2024-01-01"
end_date = "2024-12-31"
interval = "1D"
language = "en"
```

## Architecture

```
┌─────────────────┐    stdio     ┌──────────────────┐    API    ┌─────────────────┐
│                 ◄──────────────► │                  │ ◄─────────────► │                 │
│   CLI Client    │               │   VNStock MCP    │               │   Vietnamese    │
│   Interface     │               │   Server         │               │   Stock APIs    │
│                 │               │   (server.py)    │               │   (Vnstock)     │
└─────────────────┘               └──────────────────┘               └─────────────────┘
       │                                   │
       │             LLM Integration       │
       └───────────────────────────────────┘
```

### Components

- **Client (`client.py`)**: Main MCP client implementation
- **Connection (`connection.py`)**: Server connection management
- **Tools (`tools.py`)**: Tool discovery and validation
- **Formatter (`formatter.py`)**: Response formatting and display
- **CLI (`cli.py`)**: Interactive command-line interface

## Error Handling

The client provides comprehensive error handling:

- **Connection Errors**: Automatic retry with user-friendly messages
- **Tool Validation**: Argument validation before execution
- **Data Errors**: Graceful handling of missing or invalid data
- **LLM Errors**: Fallback to direct tool calls if LLM fails

## Development

This project uses uv for dependency management and development workflow.

### Development Commands

```bash
# Install development dependencies
uv sync --group dev

# Run tests
uv run --group dev python -m pytest

# Format code
uv run --group dev python -m black .

# Lint code
uv run --group dev ruff check .

# Type checking
uv run --group dev python -m mypy .

# Add new dependencies
uv add new-package

# Add development dependencies
uv add --dev new-dev-package
```

### Project Structure

```
vnstock-mcp/
├── pyproject.toml          # Project configuration and dependencies
├── server.py               # Main MCP server
├── client.py               # CLI client (if exists)
├── tests/                  # Test suite
├── .venv/                  # uv-managed virtual environment
├── uv.lock                 # Dependency lock file
└── README.md               # This file
```

## Claude Desktop Integration

To use this MCP server with Claude Desktop, add the following configuration to your Claude Desktop config file (`~/Library/Application Support/Claude/claude_desktop_config.json` on macOS):

```json
{
  "mcpServers": {
    "vnstock-mcp": {
      "command": "uv",
      "args": [
        "--directory",
        "/ABSOLUTE/PATH/TO/vnstock-mcp",
        "run",
        "server.py"
      ]
    }
  }
}
```

**Note:** Replace `/ABSOLUTE/PATH/TO/vnstock-mcp` with the actual absolute path to your project directory.

### Configuration Details
- **Server Name:** `vnstock-mcp` (unique identifier for Claude Desktop)
- **Command:** Uses `uv --directory <path> run server.py` for proper dependency management
- **Directory:** Sets working directory to ensure proper module resolution
- **Transport:** Uses stdio (standard MCP communication)

After adding the configuration, restart Claude Desktop to load the new server. You'll then have access to all 20 Vietnamese stock market tools directly in Claude Desktop, including:

> **Migration Note:** If you were previously using this server with the name "vnprices-mcp", please update your configuration to use "vnstock-mcp" instead.

- Stock, forex, crypto, and index historical data
- Financial statements and company analysis
- Portfolio optimization tools
- Mutual fund information
- Gold prices and exchange rates

## Advanced Usage

### Custom Tool Arguments

You can call tools with complex arguments:

```bash
# Tool call with JSON arguments
> call optimize_portfolio --symbols '["VNM","FPT","HPG"]' --start_date 2024-01-01

# Tool call with array
> call get_company_info --symbol FPT --info_type overview
```

### History and Auto-completion

The client maintains command history and provides auto-completion:

- **History**: Commands are saved to `~/.vnstock_history`
- **Auto-completion**: Tab completion for tool names
- **Navigation**: Arrow keys for command history

### Debug Mode

Enable debug logging for troubleshooting:

```bash
python client.py --debug
```

## Dependencies

This project uses uv for modern Python dependency management. All dependencies are managed through `pyproject.toml`:

### Core Dependencies
- `fastmcp>=2.0.0` - FastMCP 2.0 server functionality
- `vnstock` - Vietnamese stock market data
- `pyportfolioopt>=1.5.6` - Portfolio optimization
- `pandas` - Data manipulation
- `anthropic>=0.34.0` - LLM integration
- `python-dotenv>=1.0.0` - Environment variable management
- `aiohttp>=3.8.0` - Async HTTP client

### Development Dependencies
- `pytest>=7.0.0` - Testing framework
- `black>=22.0.0` - Code formatting
- `ruff>=0.1.0` - Linting and formatting
- `mypy>=1.0.0` - Type checking

### Installation
```bash
# Install all dependencies (including dev tools)
uv sync --group dev

# Install just production dependencies
uv sync
```

## Troubleshooting

### Connection Issues

1. **Server not found**: Ensure `server.py` exists and is executable
2. **Path issues**: Use absolute paths or specify `--server-path`
3. **Permission errors**: Check file permissions for server.py

### LLM Issues

1. **API key missing**: Set `ANTHROPIC_API_KEY` in `.env`
2. **Rate limits**: Anthropic API has usage limits
3. **Network issues**: Check internet connectivity

### Tool Execution Errors

1. **Invalid arguments**: Check tool schemas with `tools` command
2. **Data availability**: Some symbols may not have data for all periods
3. **Date formats**: Use YYYY-MM-DD format for dates

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Submit a pull request

## License

This project is part of the vnstock-mcp ecosystem. See the main repository for licensing information.
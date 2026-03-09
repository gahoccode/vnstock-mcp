# VNStock MCP Server

The unofficial MCP server that provides all the features of vnstock, allowing you to interact with your Claude Desktop using natural language processing capabilities.

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

**For End Users (Recommended)**
```bash
# Install from PyPI and run directly
uvx vnstock-mcp@latest
```

**For Developers**
```bash
# Clone the repository
git clone https://github.com/gahoccode/vnstock-mcp.git
cd vnstock-mcp

# Install uv if you don't have it
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install dependencies
uv sync
```

### 2. Run the Server

**End Users (uvx method)**
```bash
# Run directly from PyPI
uvx vnstock-mcp@latest
```

**Developers (local development)**
```bash
# Run from source
uv run python src/vnstock_mcp/server.py
```

## Usage Examples

```
> What's the current price of VNM stock?
> Show me FPT's financial statements for 2024
> Get the latest SJC gold price
> What are HPG's key financial ratios?
> Get VCB exchange rates for today
```

### Project Structure

```
vnstock-mcp/
├── pyproject.toml          # Project configuration and dependencies
├── src/
│   └── vnstock_mcp/        # Python package
│       ├── __init__.py     # Package initialization
│       └── server.py       # Main MCP server
├── tests/                  # Test suite
│   ├── __init__.py
│   └── conftest.py         # Pytest configuration
├── dist/                   # Built packages
│   ├── vnstock_mcp-0.1.5-py3-none-any.whl
│   └── vnstock_mcp-0.1.5.tar.gz
├── sample questions/       # Usage examples
│   └── questions.md
├── uv.lock                 # Dependency lock file
└── README.md               # This file
```

## uv vs uvx: Which to Use?

### **uvx (Recommended for Users)**
- **Purpose**: Run Python packages directly from PyPI
- **Use case**: End users who just want to use the MCP server
- **Command**: `uvx vnstock-mcp@latest`
- **Benefits**:
  - No local setup required
  - Automatic dependency management
  - Isolated execution environment

### **uv (Recommended for Developers)**
- **Purpose**: Python project and package management
- **Use case**: Developers who want to modify/contribute to the code
- **Command**: `uv run python src/vnstock_mcp/server.py`
- **Benefits**:
  - Full source code access
  - Development workflow
  - Ability to make changes

## Claude Desktop Integration

To use this MCP server with Claude Desktop, add the following configuration to your Claude Desktop config file (`~/Library/Application Support/Claude/claude_desktop_config.json` on macOS):

**Method 1: Using uvx (if PATH configured)**
```json
{
  "mcpServers": {
    "vnstock-mcp": {
      "command": "uvx",
      "args": ["vnstock-mcp"]
    }
  }
}
```

**Method 2: Using uvx (if PATH NOT configured)**
```json
{
  "mcpServers": {
    "vnstock-mcp": {
      "command": "/Users/YOUR_USERNAME/.local/bin/uvx",
      "args": ["vnstock-mcp"]
    }
  }
}
```

**Method 3: Development from source (script path)**
```json
{
  "mcpServers": {
    "vnstock-mcp": {
      "command": "uv",
      "args": [
        "--directory",
        "/Users/USERNAME/PATH_TO/src/vnstock_mcp",
        "run",
        "server.py"
      ]
    }
  }
}
```

**Method 4: Development from source (Python module)**
```json
{
  "mcpServers": {
    "vnstock-mcp": {
      "command": "uv",
      "args": [
        "--directory",
        "/Users/USERNAME/PATH_TO/vnstock-mcp",
        "run",
        "python",
        "-m",
        "vnstock_mcp.server"
      ]
    }
  }
}
```

**Note:**
- Replace `YOUR_USERNAME` with your actual username in Method 2
- Replace `USERNAME` and `PATH_TO` with your actual username and path in Method 3 and 4
- After quitting and restarting Claude Desktop, if it still can't detect the mcp server, check if `uvx` is in your PATH. If not, add `~/.local/bin` to your PATH:

```bash
# For zsh (macOS default)
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc

# For bash
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

## Publishing to PyPI

For maintainers, use the automated publish script:

```bash
# Set UV_PUBLISH_TOKEN in .env file, then run:
python dev/publish.py
```

Or publish manually:

```bash
uv publish --token $UV_PUBLISH_TOKEN
```

## License

This project is part of the vnstock-mcp ecosystem. See the main repository for licensing information.
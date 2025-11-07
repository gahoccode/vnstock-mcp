# VNStock MCP Server

The unofficial MCP server that provides all the features of vnstock, allowing you to interact with your Claude Desktop using natural language processing capabilities.

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/gahoccode/vnstock-mcp)

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
uvx vnstock-mcp
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
uvx vnstock-mcp
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
> Show me dividend history for ACB stock
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
│   ├── vnstock_mcp-0.1.0-py3-none-any.whl
│   └── vnstock_mcp-0.1.0.tar.gz
├── sample questions/       # Usage examples
│   └── questions.md
├── uv.lock                 # Dependency lock file
└── README.md               # This file
```

## uv vs uvx: Which to Use?

### **uvx (Recommended for Users)**
- **Purpose**: Run Python packages directly from PyPI
- **Use case**: End users who just want to use the MCP server
- **Command**: `uvx vnstock-mcp`
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

### Using Proxy Server (Recommended for Remote MCP)

**What is proxy_server.py?**

The `proxy_server.py` acts as a local bridge between Claude Desktop (which requires stdio transport) and your remote MCP server on Render (which uses HTTP transport):

```
Claude Desktop (stdio) ←→ proxy_server.py ←→ Remote MCP Server (HTTP)
```

**Step 1: Configure the Proxy Server**

Edit `proxy_server.py` and update the URL to point to your Render deployment:

```python
from fastmcp import FastMCP

# Create a proxy to a remote server
proxy = FastMCP.as_proxy(
    "https://vnstock-mcp.onrender.com/mcp",  # ← Replace with your Render URL
    name="Remote Server Proxy"
)

if __name__ == "__main__":
    proxy.run()  # Runs via STDIO for Claude Desktop
```

**Step 2: Configure Claude Desktop**

Add this configuration to your Claude Desktop config file:
- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "vnstock-mcp-remote": {
      "command": "uv",
      "args": [
        "--directory",
        "/Users/YOUR_USERNAME/path/to/vnstock-mcp",
        "run",
        "proxy_server.py"
      ]
    }
  }
}
```

**Important:**
- Replace `/Users/YOUR_USERNAME/Projects/vnstock-mcp` with your actual project path
- Replace `https://vnstock-mcp.onrender.com/mcp` in `proxy_server.py` with your Render URL
- Restart Claude Desktop after saving the configuration

**Step 3: Verify Connection**

After restarting Claude Desktop, look for the MCP server icon (🔌) to confirm successful connection.

---

### Video Tutorial

📺 **[Watch: How to Configure Claude Desktop with Remote MCP Server on Render](https://www.youtube.com/watch?v=NexhEJ0OcfA)**

This tutorial shows you step-by-step how to configure Claude Desktop to connect to your remote MCP server hosted on Render.

### Remote HTTP Server (Recommended - v0.2.0+)

Connect to the deployed server at: `https://vnstock-mcp.onrender.com/mcp`

**Note:**
- HTTP transport is the replacement for the deprecated SSE transport
- Use `/mcp` endpoint (not `/sse`)
- Replace `vnstock-mcp.onrender.com` with your actual Render service URL if you deployed your own instance
- No local configuration needed - access directly via HTTP endpoint

---

### Local stdio Transport (Requires code modification)

⚠️ **Important:** To use local stdio transport with uvx/uv, you must modify `server.py`:
```python
# In src/vnstock_mcp/server.py line 1116, change:
mcp.run(transport="http")  # Current
# To:
mcp.run(transport="stdio")  # or mcp.run() - stdio is default
```

Add the following configuration to your Claude Desktop config file (`~/Library/Application Support/Claude/claude_desktop_config.json` on macOS):

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

**Method 3: Development from source**

First, get your project path by running:
```bash
cd ~/path/to/vnstock-mcp/src/vnstock_mcp
pwd
```

This will output your full path (e.g., `/Users/yourusername/path/to/vnstock-mcp/src/vnstock_mcp`). Use this path in the configuration below:

```json
{
  "mcpServers": {
    "vnstock-mcp": {
      "command": "uv",
      "args": [
        "--directory",
        "/Users/yourusername/path/to/vnstock-mcp/src/vnstock_mcp",
        "run",
        "server.py"
      ]
    }
  }
}
```

**Important:** Replace `/Users/yourusername/path/to/vnstock-mcp/src/vnstock_mcp` with the actual path from your `pwd` output.

**Note:**
- Replace `YOUR_USERNAME` with your actual username in Method 2
- Replace `USERNAME` with your actual username in Method 3
- After quitting and restarting Claude Desktop, if it still can't detect the mcp server, check if `uvx` is in your PATH. If not, add `~/.local/bin` to your PATH:

```bash
# For zsh (macOS default)
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc

# For bash
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

## Generating Your Own MCP JSON Configuration

Rather than manually creating configuration files, you can automatically generate standard MCP JSON configurations using the `fastmcp` CLI tool. This approach ensures compatibility across different MCP clients.

### Quick Generation

1. Clone the repository (if you haven't already):
```bash
git clone https://github.com/gahoccode/vnstock-mcp.git
cd vnstock-mcp
```

2. Navigate to the directory containing `server.py`:
```bash
cd src/vnstock_mcp
```

3. Generate the standard MCP configuration:
```bash
fastmcp install mcp-json server.py > mcp-config.json
```

This outputs a configuration object ready to be integrated into your client's config file.

### Generated Configuration Example

Running the above command generates output like:

```json
{
  "vnstock": {
    "command": "uv",
    "args": [
      "run",
      "--with",
      "fastmcp",
      "fastmcp",
      "run",
      "/Users/yourusername/path/to/vnstock-mcp/src/vnstock_mcp/server.py"
    ]
  }
}
```

**Important:** The path shown will be the actual absolute path from your `pwd` output. Use the exact path generated by fastmcp in your configuration.

### Integrating with Claude Desktop

After generating the configuration using the Quick Generation steps above:

1. Copy the generated `vnstock` server object from the output
2. Open your Claude Desktop config file:
   - **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

3. Merge into your `mcpServers` object:
```json
{
  "mcpServers": {
    "vnstock": {
      "command": "uv",
      "args": [
        "run",
        "--with",
        "fastmcp",
        "fastmcp",
        "run",
        "/Users/yourusername/path/to/vnstock-mcp/src/vnstock_mcp/server.py"
      ]
    }
  }
}
```

4. Restart Claude Desktop

### Advanced Configuration Options

**Custom Server Name:**
```bash
fastmcp install mcp-json server.py --name "Vietnamese Stock Data"
```

**With Environment Variables:**
```bash
# Set specific environment variables
fastmcp install mcp-json server.py --env PORT=8001 --env DEBUG=false

# Load from .env file
fastmcp install mcp-json server.py --env-file .env
```

**With Python Management:**
```bash
fastmcp install mcp-json server.py --python 3.11
```

**Copy to Clipboard:**
```bash
# Requires pyperclip package
pip install pyperclip
fastmcp install mcp-json server.py --copy
```

### Configuration Structure Reference

Each generated server configuration follows this standard structure:

```json
{
  "server-name": {
    "command": "executable",
    "args": ["arg1", "arg2"],
    "env": {"VAR": "value"}
  }
}
```

**Fields:**
- **command** (required): The executable or system command to run
- **args** (optional): Array of command-line arguments in order
- **env** (optional): Environment variables to pass to the server

### Important Notes

- **Always run `fastmcp install mcp-json server.py` from the `src/vnstock_mcp` directory** (where `server.py` is located)
- All generated file paths are absolute paths to ensure portability
- Replace `<YOUR_USERNAME>` placeholders with your actual username and path
- The `uv` package manager must be installed and in your system PATH
- The `fastmcp` CLI tool handles path resolution automatically
- Configuration follows the standard MCP ecosystem format, compatible with Claude Desktop, Cursor, VS Code, and other MCP clients
- After adding configuration, restart your client application for changes to take effect

For more information and advanced options, visit the [FastMCP MCP JSON Configuration Documentation](https://gofastmcp.com/integrations/mcp-json-configuration#basic-usage).

## License

This project is part of the vnstock-mcp ecosystem. See the main repository for licensing information.
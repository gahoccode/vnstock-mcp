The unofficial MCP server that provides Vietnamese stock market financial data, allowing you to interact with your Claude Desktop using natural language processing capabilities.

## Features

- **Dual Transport Support**: Auto-detects STDIO (local) or HTTP (cloud) transport
- **Cloud Deployment**: One-click deploy to Render.com free tier
- **LLM-Powered**: Natural language processing with Anthropic Claude
- **Beautiful Output**: Formatted tables, charts, and data visualization
- **Tool Management**: Automatic tool discovery and validation
- **Smart Parsing**: Vietnamese stock symbol and date format support
- **Error Handling**: Robust error recovery and user-friendly messages

## Quick Start

```bash
# Install from PyPI and run directly
uvx vnstock-mcp@latest
```

## Usage Examples

```
> Show me FPT's income statements for 2024
> What are HPG's key financial ratios?
```

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

**Method 5: Docker MCP Gateway (simple)**

```json
{
  "mcpServers": {
    "MCP_DOCKER": {
      "type": "stdio",
      "command": "docker",
      "args": ["mcp", "gateway", "run"]
    }
  }
}
```

**Method 6: Docker MCP Gateway (explicit catalog/registry)**

```json
{
  "mcpServers": {
    "mcp-toolkit-gateway": {
      "command": "docker",
      "args": [
        "run",
        "-i",
        "--rm",
        "-v",
        "/var/run/docker.sock:/var/run/docker.sock",
        "-v",
        "/Users/YOUR_USERNAME/.docker/mcp:/mcp",
        "docker/mcp-gateway",
        "--catalog=/mcp/catalogs/vnstock.yaml",
        "--config=/mcp/config.yaml",
        "--registry=/mcp/registry.yaml",
        "--transport=stdio"
      ]
    }
  }
}
```

**Note:**

- Replace `YOUR_USERNAME` with your actual username in Methods 2 and 6
- Replace `USERNAME` and `PATH_TO` with your actual username and path in Methods 3 and 4
- Methods 5 and 6 require [Docker Desktop](https://www.docker.com/products/docker-desktop/) with the MCP Toolkit enabled. See [Setup Guide](docs/setup-guide.md) for details
- Method 5 lets Docker manage catalogs automatically; Method 6 pins specific catalog, config, and registry files
- After quitting and restarting Claude Desktop, if it still can't detect the mcp server, check if `uvx` is in your PATH. If not, add `~/.local/bin` to your PATH:

```bash
# For zsh (macOS default)
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc

# For bash
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

Claude Code Integration

```bash
claude mcp add vnstock-mcp --transport http https://your-app.onrender.com/mcp
```

## Remote MCP Server

Connect to a hosted VNStock MCP server deployed on Render (or any cloud provider) without installing anything locally. The remote server exposes a Streamable HTTP endpoint at `/mcp`.

Use the server URL `https://your-app.onrender.com/mcp` when adding the remote MCP server in each client's GUI. Guides per client:

- **Claude Desktop** — Add via Settings > MCP Servers
- **Claude Code (CLI)** — `claude mcp add vnstock-mcp https://your-app.onrender.com/mcp --transport http`
- **Perplexity** — Follow [Adding Custom Remote Connectors](https://www.perplexity.ai/help-center/en/articles/13915507-adding-custom-remote-connectors)

**Note:** Replace `your-app.onrender.com` with your actual Render deployment URL and add `/mcp` at the end.

You can verify the server is running with a custom health endpoint `/health` like this :

```bash
curl https://your-app.onrender.com/health
```

## Development

Setup the docker mcp gateway [Setup Guide](docs/setup-guide.md)

Project structure, Docker builds, and deployment guides, see [Development Guide](docs/DEVELOPMENT.md).

Tips on fixing common issues include Quick diagonostic commands,verifying catalogs, registry, validating Claude Config, Authentication and Permission [Troubleshooting Guide](docs/troubleshoot.md)

## License

This project is wrapper of the vnstock library. See the main repository for licensing information.

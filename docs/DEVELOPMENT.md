# Development Guide

This guide covers developer setup, project internals, Docker builds, and deployment. For end-user installation and usage, see the [README](../README.md).

## Developer Setup

```bash
# Clone the repository
git clone https://github.com/gahoccode/vnstock-mcp.git
cd vnstock-mcp

# Install uv if you don't have it
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install dependencies
uv sync
```

### Run from Source

```bash
uv run python src/vnstock_mcp/server.py
```

## Project Structure

```
vnstock-mcp/
├── pyproject.toml          # Project configuration and dependencies
├── Dockerfile              # Multi-stage Docker build
├── docker-compose.yml      # Standalone container deployment
├── docker-compose.gateway.yml  # Docker MCP Gateway deployment
├── docker/                 # Gateway configuration
│   ├── vnstock.yaml        # Server entry for gateway
│   ├── registry.yaml       # Gateway registry
│   └── config.yaml         # Gateway config
├── render.yaml             # Render.com native Python deployment
├── render-gateway.yaml     # Render.com Docker deployment
├── src/
│   └── vnstock_mcp/        # Python package
│       ├── __init__.py     # Package initialization
│       ├── server.py       # MCP server (API Layer)
│       ├── config.py       # Configuration constants
│       ├── exceptions.py   # Custom exceptions
│       ├── core/           # Service Layer (business logic)
│       │   ├── base.py     # BaseService with async patterns
│       │   ├── financial.py
│       │   ├── company.py
│       │   └── fund.py
│       ├── models/         # Model Layer (result types)
│       │   ├── base.py     # ServiceResult, DataFrameResult
│       │   ├── financial.py
│       │   ├── company.py
│       │   └── fund.py
│       └── utils/          # Utility functions
│           └── data_transform.py
├── docs/                   # Documentation
│   ├── ARCHITECTURE.md     # System architecture overview
│   ├── DEVELOPMENT.md      # This file
│   └── adr/                # Architecture Decision Records
│       ├── 001-layered-architecture.md
│       ├── 002-result-objects.md
│       └── 003-lazy-imports.md
├── tests/                  # Test suite
│   ├── __init__.py
│   └── conftest.py         # Pytest configuration
├── dist/                   # Built packages
├── sample questions/       # Usage examples
├── uv.lock                 # Dependency lock file
└── README.md               # End-user documentation
```

For detailed architecture documentation, see [ARCHITECTURE.md](ARCHITECTURE.md).

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

## Docker

### Build the Image

```bash
docker build -t vnstock-mcp:latest .
```

### Run Standalone (HTTP Mode)

```bash
docker compose up
```

Test with: `curl http://localhost:8001/health`

### Run with Docker MCP Gateway

The server integrates with [Docker MCP Gateway](https://github.com/docker/mcp-gateway) for container-isolated MCP serving.

```bash
# Start the gateway with vnstock-mcp registered
docker compose -f docker-compose.gateway.yml up
```

The gateway listens on port 8811 and starts vnstock-mcp containers on demand.

### Run in STDIO Mode

When no `PORT` environment variable is set, the server uses STDIO transport (compatible with Docker MCP Gateway's on-demand container model):

```bash
docker run -i --rm vnstock-mcp:latest
```

### Docker MCP Toolkit (Docker Desktop)

If you have Docker Desktop with the MCP Toolkit extension:

```bash
# Connect Claude Code to Docker MCP Gateway
claude mcp add MCP_DOCKER -s user -- docker mcp gateway run
```

### Deploy to Render (Docker)

A separate Render Blueprint using the Dockerfile is available:

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/gahoccode/vnstock-mcp)

Use `render-gateway.yaml` for Docker-based deployment (the existing `render.yaml` uses Render's native Python runtime).

## Publishing to PyPI

For maintainers, use the automated publish script:

```bash
# Set UV_PUBLISH_TOKEN in .env file, then run:
uv run dev/publish.py
```

Or publish manually:

```bash
uv publish --token $UV_PUBLISH_TOKEN
```

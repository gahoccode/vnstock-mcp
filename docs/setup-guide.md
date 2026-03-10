# Quick Start Guide - 5 Minutes to Your First MCP Server

Get your first MCP server running in under 5 minutes!

## Prerequisites Check (30 seconds)

**Docker Desktop** installed and running  
**Claude Desktop** installed  
Terminal/Command Prompt open

## Step 1: Enable Docker MCP Toolkit (1 minute)

1. Open Docker Desktop
2. Go to **Settings** → **Beta Features**
3. Enable **"Docker MCP Toolkit"**
4. Click **Apply & Restart**

## Step 2: Build the vnstock mcp server

```bash
# Clone this repository (or download the ZIP)
git clone https://github.com/gahoccode/vnstock-mcp.git
cd vnstock-mcp

# Build the Docker image
docker build -t vnstock-mcp:latest
```

## Step 3: Create Custom Catalog (1 minute)

```bash
# Create the catalogs directory
mkdir -p ~/.docker/mcp/catalogs

# Create custom catalog file
cat > ~/.docker/mcp/catalogs/custom.yaml << 'EOF'
version: 2
name: custom
displayName: Custom MCP Servers
registry:
  vnstock-mcp:
    description: "pull finanancial data using vnstock library"
    title: "vnstock-mcp"
    type: server
    dateAdded: "2025-01-01T00:00:00Z"
    image: vnstock-mcp:latest
    ref: ""
    tools:
      - name: get_income_statement
        description: "Get annual income statement for Vietnamese stocks"
      - name: get_balance_sheet
        description: "Get annual balance sheet for Vietnamese stocks"
      - name: get_cash_flow
        description: "Get annual cash flow statement for Vietnamese stocks"
      - name: get_financial_ratios
        description: "Get annual financial ratios for Vietnamese stocks"
      - name: get_company_info
        description: "Get company information (overview, shareholders, officers, etc.)"
      - name: get_fund_listing
        description: "Get list of all available mutual funds"
      - name: search_funds
        description: "Search for mutual funds by symbol or name"
      - name: get_fund_nav_report
        description: "Get historical NAV report for a mutual fund"
      - name: get_fund_top_holdings
        description: "Get top 10 holdings for a mutual fund"
      - name: get_fund_industry_allocation
        description: "Get industry allocation for a mutual fund"
      - name: get_fund_asset_allocation
        description: "Get asset allocation for a mutual fund"
    metadata:
      category: productivity
      tags:
        - finance
        - vnstock
        - statements
EOF
```

## Step 4: Update Registry (30 seconds)

```bash
# Add to registry
echo "  vnstock-mcp:" >> ~/.docker/mcp/registry.yaml
echo '    ref: ""' >> ~/.docker/mcp/registry.yaml
```

## Step 5: Configure Claude Desktop (1 minute)

### macOS:

```bash
# Edit Claude config
nano ~/Library/Application\ Support/Claude/claude_desktop_config.json
```

### Windows (PowerShell):

```powershell
# Edit Claude config
notepad "$env:APPDATA\Claude\claude_desktop_config.json"
```

Add this configuration (replace `[YOUR_USERNAME]` with your actual username):

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
        "/Users/[YOUR_USERNAME]/.docker/mcp:/mcp",
        "docker/mcp-gateway",
        "--catalog=/mcp/catalogs/docker-mcp.yaml",
        "--catalog=/mcp/catalogs/custom.yaml",
        "--config=/mcp/config.yaml",
        "--registry=/mcp/registry.yaml",
        "--tools-config=/mcp/tools.yaml",
        "--transport=stdio"
      ]
    }
  }
}
```

**Note for Windows:** Use `C:\\Users\\[YOUR_USERNAME]` with double backslashes

## Troubleshooting

**Tools not appearing?**

- Make sure Docker Desktop is running
- Verify the Docker image built successfully: `docker images | grep vnstock`
- Check Claude logs: Help → Show Logs

**Permission errors?**

- Make sure Docker Desktop has necessary permissions
- On Mac: System Preferences → Security & Privacy

**Still stuck?**

- Check the full [troubleshooting guide](../docs/troubleshooting.md)
- Watch the video tutorial for visual guidance

## What's Next?

- Explore the [Docker MCP Gateway](../docs/docker-gateway.md)

---

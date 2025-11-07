# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Changed
- Updated render.yaml to use `runtime: python` for schema compliance
- Optimized monorepo build configuration with targeted build filters

## [0.2.0] - 2025-01-07

### Changed
- **BREAKING**: Migrated from stdio transport (local uvx) to HTTP transport (remote server)
  - Server now runs as remote HTTP service instead of local process
  - Upgraded to FastMCP 2.0 HTTP transport implementation
  - Deployed to Render platform (Singapore region) for production accessibility
  - Users must update Claude Desktop configuration from uvx command to HTTP endpoint
  - Port configuration via PORT environment variable (defaults to 8001)
  - Host binding to 0.0.0.0 for external access

### Added
- **Portfolio optimization tools** using PyPortfolioOpt library (3 new tools):
  - `calculate_returns`: Calculate expected returns for portfolio of stocks
    - Supports mean historical and EMA historical methods
    - Configurable log returns vs arithmetic returns
    - 252-day frequency for annualized calculations
  - `optimize_portfolio`: Mean-variance optimization for maximum Sharpe ratio
    - Configurable risk-free rate
    - Multiple covariance methods: sample_cov, ledoit_wolf, exp_cov, semicovariance
    - Returns optimal weights and performance metrics
  - `full_portfolio_optimization`: Multi-strategy portfolio optimization
    - Max Sharpe ratio strategy
    - Minimum volatility strategy
    - Maximum utility strategy (configurable risk aversion)
    - Comprehensive comparison across all strategies
- Render deployment configuration via render.yaml
  - Monorepo support with build filters
  - Environment variable configuration
  - Auto-deploy triggers
- Remote server production deployment capabilities

### Fixed
- Lambda loop variable capture in async operations to prevent late binding issues
- Proper async event loop management for portfolio calculations

### Migration Notes
- **Before (0.1.0)**: Local execution via `uvx vnstock-mcp` with stdio transport
- **After (0.2.0)**: Remote HTTP server at render.com, accessed via HTTP endpoint
- Claude Desktop configuration changed from local command to remote HTTP URL

## [0.1.0] - 2024-12-XX

### Added
- Initial release of VNStock MCP Server with local stdio transport
- 22 MCP tools across 6 categories:
  - **Market Data**: Stock history, forex, crypto, indices data (4 tools)
  - **Financial Analysis**: Income statements, balance sheets, cash flows, ratios, dividends (5 tools)
  - **Company Information**: Overview, shareholders, officers, subsidiaries, events, news, reports (9 subtypes)
  - **Precious Metals**: SJC and BTMC gold prices (2 tools)
  - **Exchange Rate**: Vietcombank exchange rates (1 tool)
  - **Fund Management**: Mutual fund listings, NAV reports, holdings, allocations (5 tools)
- Async architecture with non-blocking operations via `loop.run_in_executor()`
- Data sources integration:
  - VCI: Primary source for stocks, financials, company info
  - MSN: Forex, crypto, international indices
  - TCBS: Dividend data
  - Direct APIs: SJC/BTMC gold prices, VCB exchange rates
- UV package manager support with uv.lock
- PyPI distribution via uvx command
- Comprehensive pytest fixtures for async testing
- Modern setuptools structure with src layout

### Documentation
- README.md with installation and usage guides
- CLAUDE.md for AI assistant development guidance
- llms.txt for LLM-specific documentation
- Claude Desktop integration examples for uvx/stdio method

## Project Links
- Repository: https://github.com/gahoccode/vnstock-mcp
- PyPI: https://pypi.org/project/vnstock-mcp/
- Render Service: vnstock-mcp-server (Singapore region)

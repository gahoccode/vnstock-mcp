# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Fixed
- **Circular import error with vnai dependency** - Replaced top-level `from vnstock import Vnstock, Quote` imports with explorer-level imports (`from vnstock.explorer.vci import Quote, Company, Finance`, `from vnstock.explorer.msn import Quote as MSNQuote`, `from vnstock.explorer.tcbs import Company as TCBSCompany`) to avoid circular dependency between vnstock and vnai modules. This resolves the `AttributeError: partially initialized module 'vnai' has no attribute 'setup'` error when running via uvx.

### Changed
- **Lazy loading for Fund objects** - Moved `Fund()` initialization from module-level (eager loading) to function-level (lazy loading) in all 6 fund management tools. This eliminates the API call to Fmarket at server startup, resulting in:
  - Faster server startup (no network I/O at import time)
  - More resilient initialization (server can start even if Fmarket API is temporarily unavailable)
  - Better separation of concerns (data fetching only happens when fund tools are actually invoked)
- **Direct class instantiation** - Replaced `Vnstock()` wrapper pattern with direct class instantiation for all data source modules:
  - Forex: `Vnstock().fx()` → `MSNQuote(symbol, source='MSN')`
  - Crypto: `Vnstock().crypto()` → `MSNQuote(symbol, source='MSN')`
  - World indices: `Vnstock().world_index()` → `MSNQuote(symbol, source='MSN')`
  - Financial statements: `Vnstock().stock().finance` → `Finance(symbol, source='VCI')`
  - Company info: `Vnstock().stock().company` → `Company(symbol, source='VCI')`
  - Dividends: `Vnstock().stock(source='TCBS').company` → `TCBSCompany(symbol)`

### Technical Details
- **Affected files**: `src/vnstock_mcp/server.py`
- **Functions modified**: 15 out of 20 MCP tools
- **Import pattern**: Explorer-level imports (`vnstock.explorer.{vci,msn,tcbs}`) instead of top-level (`vnstock`)
- **Compatibility**: No breaking changes to tool signatures or behavior

## [0.1.0] - 2024-11-06

### Added
- Initial release with 20 MCP tools across 6 categories:
  - Market Data Tools (4): Stock, forex, crypto, and index historical data
  - Financial Analysis Tools (4): Income statements, balance sheets, cash flows, financial ratios
  - Company Information Tools (2): Dividend history, company info (8 sub-types)
  - Precious Metals Tools (2): SJC and BTMC gold prices
  - Exchange Rate Tools (1): VCB exchange rates
  - Fund Management Tools (5): Fund listings, NAV reports, holdings, allocations
- FastMCP 2.0 integration for Claude Desktop
- Async architecture with proper event loop management
- Support for multiple data sources (VCI, MSN, TCBS, direct APIs)

[Unreleased]: https://github.com/gahoccode/vnstock-mcp/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/gahoccode/vnstock-mcp/releases/tag/v0.1.0

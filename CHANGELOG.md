# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Fixed
- **Hardcoded source parameter in Finance and Company classes** - Removed hardcoded `source="VCI"` parameter from Finance and Company class instantiations. The `source` parameter is not valid for explorer-level classes (`vnstock.explorer.vci.Finance` and `vnstock.explorer.vci.Company`), which are already VCI-specific by their module path. This fix prevents potential initialization errors and aligns with the vnstock library's API design.
  - **Affected functions**:
    - `get_income_statement()` - Finance initialization (line 221)
    - `get_balance_sheet()` - Finance initialization (line 261)
    - `get_cash_flow()` - Finance initialization (line 301)
    - `get_financial_ratios()` - Finance initialization (line 342)
    - `get_company_info()` - Company initialization (line 527)
  - **Impact**: All 5 functions now correctly instantiate Finance/Company classes without invalid parameters
  - **Scope**: Bug fix, no breaking changes to tool behavior or API

- **Circular import error with vnai dependency** - Implemented lazy imports for all vnstock modules to avoid circular dependency. All imports from `vnstock.explorer.*` are now moved inside function bodies instead of module-level. This resolves the `AttributeError: partially initialized module 'vnai' has no attribute 'setup'` error when running via uvx.
  - **Root cause**: Any import from `vnstock.*` (even explorer-level) triggers `vnstock/__init__.py` execution, which imports vnai and calls `vnai.setup()`, creating a circular dependency before vnai is fully initialized.
  - **Solution**: Lazy imports - all vnstock imports are deferred until function execution, avoiding module-level initialization.

### Changed
- **Lazy imports for all vnstock modules** - Moved ALL vnstock imports from module-level to function-level across all 20 MCP tools:
  - Market Data tools (4): `Quote` from vci, `MSNQuote` from msn
  - Financial Analysis tools (4): `Finance` from vci, `flatten_hierarchical_index` from core.utils
  - Company Information tools (2): `Company` from vci, `TCBSCompany` from tcbs
  - Precious Metals tools (2): `sjc_gold_price`, `btmc_goldprice` from misc.gold_price
  - Exchange Rate tool (1): `vcb_exchange_rate` from misc.exchange_rate
  - Fund Management tools (6): `Fund` from fmarket.fund
- **Quote class initialization fix** - Removed invalid `source` parameter from explorer-level Quote instantiation (explorer classes don't accept source parameter)
- **Removed module-level Fund() initialization** - Eliminated eager API call at server startup by moving `Fund()` instantiation inside each fund function

### Technical Details
- **Affected files**: `src/vnstock_mcp/server.py`
- **Functions modified**: All 20 MCP tools
- **Import pattern**: Lazy imports inside try blocks with comment `# Lazy import to avoid circular dependency`
- **Performance impact**: Minimal - first call to each function slightly slower, subsequent calls use cached imports
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

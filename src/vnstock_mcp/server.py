"""
Vietnamese Stock Market Data MCP Server
Provides tools to fetch financial statements, company information, and fund data from vnstock
"""

from fastmcp import FastMCP
from starlette.responses import JSONResponse

from vnstock_mcp.config import PORT, SERVICE_NAME, USE_HTTP, VERSION
from vnstock_mcp.core.company import CompanyService
from vnstock_mcp.core.financial import FinancialService
from vnstock_mcp.core.fund import FundService

# Initialize the MCP server
mcp = FastMCP(SERVICE_NAME)

# Initialize services
financial_service = FinancialService()
company_service = CompanyService()
fund_service = FundService()


@mcp.custom_route("/health", methods=["GET"])
async def health_check(request):
    """Health check endpoint for monitoring and load balancer health probes."""
    return JSONResponse({
        "status": "healthy",
        "service": SERVICE_NAME,
        "version": VERSION
    })


# ========== Financial Analysis Tools ==========


@mcp.tool()
async def get_income_statement(symbol: str, lang: str = "en") -> str:
    """
    Get annual income statement (profit & loss) for Vietnamese stocks with chronological year ordering.

    Args:
        symbol: Stock ticker symbol (e.g., 'VCI', 'VNM', 'HPG')
        lang: Language - 'en' (English) or 'vi' (Vietnamese')

    Returns:
        JSON string with annual income statement data including revenue, expenses,
        profit metrics, and earnings per share (EPS) for multiple years, sorted chronologically
    """
    result = await financial_service.get_income_statement(symbol.upper(), lang)
    return result.to_json()


@mcp.tool()
async def get_balance_sheet(symbol: str, lang: str = "en") -> str:
    """
    Get annual balance sheet for Vietnamese stocks with chronological year ordering.

    Args:
        symbol: Stock ticker symbol (e.g., 'VCI', 'VNM', 'HPG')
        lang: Language - 'en' (English) or 'vi' (Vietnamese)

    Returns:
        JSON string with annual balance sheet data including assets, liabilities,
        equity, and detailed financial position metrics for multiple years, sorted chronologically
    """
    result = await financial_service.get_balance_sheet(symbol.upper(), lang)
    return result.to_json()


@mcp.tool()
async def get_cash_flow(symbol: str, lang: str = "en") -> str:
    """
    Get annual cash flow statement for Vietnamese stocks with chronological year ordering.

    Args:
        symbol: Stock ticker symbol (e.g., 'VCI', 'VNM', 'HPG')
        lang: Language - 'en' (English) or 'vi' (Vietnamese)

    Returns:
        JSON string with annual cash flow data including operating, investing,
        and financing activities for multiple years, sorted chronologically
    """
    result = await financial_service.get_cash_flow(symbol.upper(), lang)
    return result.to_json()


@mcp.tool()
async def get_financial_ratios(symbol: str, lang: str = "en") -> str:
    """
    Get annual financial ratios and metrics for Vietnamese stocks with chronological year ordering.

    Args:
        symbol: Stock ticker symbol (e.g., 'VCI', 'VNM', 'HPG')
        lang: Language - 'en' (English) or 'vi' (Vietnamese)

    Returns:
        JSON string with annual financial ratios including P/B (Price-to-Book),
        ROE (Return on Equity), and other key financial health indicators, sorted chronologically
    """
    result = await financial_service.get_financial_ratios(symbol.upper(), lang)
    return result.to_json()


# ========== Company Information Tools ==========


@mcp.tool()
async def get_company_info(
    symbol: str, info_type: str = "overview", lang: str = "en"
) -> str:
    """
    Get company information for Vietnamese stocks.

    Args:
        symbol: Stock ticker symbol (e.g., 'VCI', 'ACB', 'HPG')
        info_type: Type of company information to fetch:
                  'overview' - Company overview and basic information
                  'shareholders' - Major shareholders information
                  'officers' - Company officers and management (filter: 'working', 'resigned', 'all')
                  'subsidiaries' - Subsidiaries and associated companies (filter: 'all', 'subsidiary')
                  'events' - Corporate events and announcements
                  'news' - Company news and updates
                  'reports' - Analysis reports
                  'ratio_summary' - Financial ratios summary
                  'trading_stats' - Trading statistics and market data
        lang: Language - 'en' (English) or 'vi' (Vietnamese)

    Returns:
        JSON string with company information based on the requested type
    """
    result = await company_service.get_company_info(symbol.upper(), info_type, lang)
    return result.to_json()


# ========== Fund Management Tools ==========


@mcp.tool()
async def get_fund_listing(fund_type: str = "") -> str:
    """
    Get list of all available mutual funds.

    Args:
        fund_type: Filter by fund type - '' (all), 'BALANCED', 'BOND', 'STOCK'

    Returns:
        JSON string with complete fund listing including fund codes, names, NAV,
        fund types, owners, inception dates, and performance metrics
    """
    result = await fund_service.get_fund_listing(fund_type)
    return result.to_json()


@mcp.tool()
async def search_funds(symbol: str) -> str:
    """
    Search for mutual funds by symbol or partial name.

    Args:
        symbol: Fund short name or ticker (case-insensitive, partial match allowed)

    Returns:
        JSON string with matching funds including their IDs and short names
    """
    result = await fund_service.search_funds(symbol)
    return result.to_json()


@mcp.tool()
async def get_fund_nav_report(symbol: str) -> str:
    """
    Get historical NAV report for a specific mutual fund.

    Args:
        symbol: Fund short name/ticker (e.g., 'SSISCA', 'VESAF')

    Returns:
        JSON string with historical NAV data including dates and NAV per unit
    """
    result = await fund_service.get_fund_nav_report(symbol.upper())
    return result.to_json()


@mcp.tool()
async def get_fund_top_holdings(symbol: str) -> str:
    """
    Get top 10 holdings for a specific mutual fund.

    Args:
        symbol: Fund short name/ticker (e.g., 'SSISCA', 'VESAF')

    Returns:
        JSON string with top holdings including stock codes, industries,
        net asset percentages, asset types, and last update date
    """
    result = await fund_service.get_fund_top_holdings(symbol.upper())
    return result.to_json()


@mcp.tool()
async def get_fund_industry_allocation(symbol: str) -> str:
    """
    Get industry allocation breakdown for a specific mutual fund.

    Args:
        symbol: Fund short name/ticker (e.g., 'SSISCA', 'VESAF')

    Returns:
        JSON string with industry allocation including industry names
        and net asset percentages
    """
    result = await fund_service.get_fund_industry_allocation(symbol.upper())
    return result.to_json()


@mcp.tool()
async def get_fund_asset_allocation(symbol: str) -> str:
    """
    Get asset allocation breakdown for a specific mutual fund.

    Args:
        symbol: Fund short name/ticker (e.g., 'SSISCA', 'VESAF')

    Returns:
        JSON string with asset allocation including asset types
        and asset percentages
    """
    result = await fund_service.get_fund_asset_allocation(symbol.upper())
    return result.to_json()


def main():
    """Main entry point for the MCP server."""
    if USE_HTTP:
        # HTTP transport for remote deployment (Render, etc.)
        mcp.run(transport="streamable-http", host="0.0.0.0", port=PORT)
    else:
        # STDIO transport for local usage (uvx, Claude Desktop)
        mcp.run()


if __name__ == "__main__":
    main()
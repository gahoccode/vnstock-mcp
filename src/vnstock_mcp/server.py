"""
Vietnamese Stock Market Data MCP Server
Provides tools to fetch financial statements, company information, and fund data from vnstock
"""

import asyncio
import os

from fastmcp import FastMCP
from starlette.responses import JSONResponse

# Detect transport mode from environment
# If PORT env var is set (e.g., by Render), use HTTP transport
# Otherwise, default to STDIO transport for local usage (uvx)
PORT = int(os.environ.get("PORT", 8001))
_use_http = "PORT" in os.environ

# Initialize the MCP server
mcp = FastMCP("vnstock")


@mcp.custom_route("/health", methods=["GET"])
async def health_check(request):
    """Health check endpoint for monitoring and load balancer health probes."""
    return JSONResponse({
        "status": "healthy",
        "service": "vnstock-mcp",
        "version": "0.2.0"
    })

# NOTE: All vnstock imports are done lazily (inside functions) to avoid circular dependency
# Importing from vnstock.* at module level triggers vnstock/__init__.py which imports vnai,
# causing a circular import error. Lazy imports solve this by deferring import until needed.


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
    try:
        # Lazy import to avoid circular dependency
        from vnstock.explorer.vci import Finance

        loop = asyncio.get_event_loop()

        # Initialize Finance with VCI source
        finance = Finance(symbol=symbol.upper())

        # Fetch annual income statement in executor to avoid blocking
        df = await loop.run_in_executor(
            None, lambda: finance.income_statement(period="year", lang=lang)
        )

        if df is None or df.empty:
            return f"No income statement data found for {symbol}"

        # Sort by yearReport for chronological analysis
        df = df.sort_values("yearReport").reset_index(drop=True)

        # Convert to JSON
        return df.to_json(orient="records", date_format="iso", indent=2)

    except Exception as e:
        return f"Error fetching income statement for {symbol}: {str(e)}"


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
    try:
        # Lazy import to avoid circular dependency
        from vnstock.explorer.vci import Finance

        loop = asyncio.get_event_loop()

        # Initialize Finance with VCI source
        finance = Finance(symbol=symbol.upper())

        # Fetch annual balance sheet in executor to avoid blocking
        df = await loop.run_in_executor(
            None, lambda: finance.balance_sheet(period="year", lang=lang)
        )

        if df is None or df.empty:
            return f"No balance sheet data found for {symbol}"

        # Sort by yearReport for chronological analysis
        df = df.sort_values("yearReport").reset_index(drop=True)

        # Convert to JSON
        return df.to_json(orient="records", date_format="iso", indent=2)

    except Exception as e:
        return f"Error fetching balance sheet for {symbol}: {str(e)}"


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
    try:
        # Lazy import to avoid circular dependency
        from vnstock.explorer.vci import Finance

        loop = asyncio.get_event_loop()

        # Initialize Finance with VCI source
        finance = Finance(symbol=symbol.upper())

        # Fetch annual cash flow statement in executor to avoid blocking
        df = await loop.run_in_executor(
            None, lambda: finance.cash_flow(period="year", lang=lang)
        )

        if df is None or df.empty:
            return f"No cash flow data found for {symbol}"

        # Sort by yearReport for chronological analysis
        df = df.sort_values("yearReport").reset_index(drop=True)

        # Convert to JSON
        return df.to_json(orient="records", date_format="iso", indent=2)

    except Exception as e:
        return f"Error fetching cash flow for {symbol}: {str(e)}"


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
    try:
        # Lazy imports to avoid circular dependency
        from vnstock.explorer.vci import Finance
        from vnstock.core.utils.transform import flatten_hierarchical_index

        loop = asyncio.get_event_loop()

        # Initialize Finance with VCI source
        finance = Finance(symbol=symbol.upper())

        # Fetch annual financial ratios in executor to avoid blocking
        df = await loop.run_in_executor(
            None, lambda: finance.ratio(period="year", lang=lang)
        )

        if df is None or df.empty:
            return f"No financial ratio data found for {symbol}"

        # Flatten MultiIndex DataFrame first, then sort chronologically
        flattened_df = await loop.run_in_executor(
            None,
            lambda: flatten_hierarchical_index(
                df, separator="_", handle_duplicates=True, drop_levels=0
            ),
        )

        # Sort flattened DataFrame by yearReport for chronological analysis
        if "yearReport" in flattened_df.columns:
            flattened_df = flattened_df.sort_values("yearReport").reset_index(drop=True)

        # Convert to JSON
        return flattened_df.to_json(orient="records", date_format="iso", indent=2)

    except Exception as e:
        return f"Error fetching financial ratios for {symbol}: {str(e)}"


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
    try:
        # Lazy import to avoid circular dependency
        from vnstock.explorer.vci import Company

        loop = asyncio.get_event_loop()

        # Initialize Company with VCI source
        company = Company(symbol=symbol.upper())

        # Fetch the requested company information in executor to avoid blocking
        if info_type == "overview":
            df = await loop.run_in_executor(None, lambda: company.overview())
        elif info_type == "shareholders":
            df = await loop.run_in_executor(None, lambda: company.shareholders())
        elif info_type == "officers":
            # Default to working officers, can be extended to accept filter parameter
            df = await loop.run_in_executor(
                None, lambda: company.officers(filter_by="working")
            )
        elif info_type == "subsidiaries":
            # Default to all subsidiaries and associated companies
            df = await loop.run_in_executor(
                None, lambda: company.subsidiaries(filter_by="all")
            )
        elif info_type == "events":
            df = await loop.run_in_executor(None, lambda: company.events())
        elif info_type == "news":
            df = await loop.run_in_executor(None, lambda: company.news())
        elif info_type == "reports":
            df = await loop.run_in_executor(None, lambda: company.reports())
        elif info_type == "ratio_summary":
            df = await loop.run_in_executor(None, lambda: company.ratio_summary())
        elif info_type == "trading_stats":
            df = await loop.run_in_executor(None, lambda: company.trading_stats())
        else:
            return f"Invalid info_type '{info_type}'. Valid types: overview, shareholders, officers, subsidiaries, events, news, reports, ratio_summary, trading_stats"

        if df is None or df.empty:
            return f"No {info_type} data found for {symbol}"

        # Convert to JSON
        return df.to_json(orient="records", date_format="iso", indent=2)

    except Exception as e:
        return f"Error fetching {info_type} for {symbol}: {str(e)}"


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
    try:
        # Lazy import to avoid circular dependency
        from vnstock.explorer.fmarket.fund import Fund

        loop = asyncio.get_event_loop()

        # Initialize Fund with lazy loading
        fund = Fund()

        # Fetch fund listing in executor to avoid blocking
        df = await loop.run_in_executor(None, lambda: fund.listing(fund_type=fund_type))

        if df is None or df.empty:
            return f"No funds found for type: {fund_type}"

        # Convert to JSON
        return df.to_json(orient="records", date_format="iso", indent=2)

    except Exception as e:
        return f"Error fetching fund listing: {str(e)}"


@mcp.tool()
async def search_funds(symbol: str) -> str:
    """
    Search for mutual funds by symbol or partial name.

    Args:
        symbol: Fund short name or ticker (case-insensitive, partial match allowed)

    Returns:
        JSON string with matching funds including their IDs and short names
    """
    try:
        # Lazy import to avoid circular dependency
        from vnstock.explorer.fmarket.fund import Fund

        loop = asyncio.get_event_loop()

        # Initialize Fund with lazy loading
        fund = Fund()

        # Search for funds in executor to avoid blocking
        df = await loop.run_in_executor(None, lambda: fund.filter(symbol=symbol))

        if df is None or df.empty:
            return f"No funds found matching: {symbol}"

        # Convert to JSON
        return df.to_json(orient="records", date_format="iso", indent=2)

    except Exception as e:
        return f"Error searching funds: {str(e)}"


@mcp.tool()
async def get_fund_nav_report(symbol: str) -> str:
    """
    Get historical NAV report for a specific mutual fund.

    Args:
        symbol: Fund short name/ticker (e.g., 'SSISCA', 'VESAF')

    Returns:
        JSON string with historical NAV data including dates and NAV per unit
    """
    try:
        # Lazy import to avoid circular dependency
        from vnstock.explorer.fmarket.fund import Fund

        loop = asyncio.get_event_loop()

        # Initialize Fund with lazy loading
        fund = Fund()

        # Fetch NAV report in executor to avoid blocking
        df = await loop.run_in_executor(
            None, lambda: fund.details.nav_report(symbol=symbol.upper())
        )

        if df is None or df.empty:
            return f"No NAV data found for fund: {symbol}"

        # Convert to JSON
        return df.to_json(orient="records", date_format="iso", indent=2)

    except Exception as e:
        return f"Error fetching NAV report for {symbol}: {str(e)}"


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
    try:
        # Lazy import to avoid circular dependency
        from vnstock.explorer.fmarket.fund import Fund

        loop = asyncio.get_event_loop()

        # Initialize Fund with lazy loading
        fund = Fund()

        # Fetch top holdings in executor to avoid blocking
        df = await loop.run_in_executor(
            None, lambda: fund.details.top_holding(symbol=symbol.upper())
        )

        if df is None or df.empty:
            return f"No top holdings data found for fund: {symbol}"

        # Convert to JSON
        return df.to_json(orient="records", date_format="iso", indent=2)

    except Exception as e:
        return f"Error fetching top holdings for {symbol}: {str(e)}"


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
    try:
        # Lazy import to avoid circular dependency
        from vnstock.explorer.fmarket.fund import Fund

        loop = asyncio.get_event_loop()

        # Initialize Fund with lazy loading
        fund = Fund()

        # Fetch industry allocation in executor to avoid blocking
        df = await loop.run_in_executor(
            None, lambda: fund.details.industry_holding(symbol=symbol.upper())
        )

        if df is None or df.empty:
            return f"No industry allocation data found for fund: {symbol}"

        # Convert to JSON
        return df.to_json(orient="records", date_format="iso", indent=2)

    except Exception as e:
        return f"Error fetching industry allocation for {symbol}: {str(e)}"


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
    try:
        # Lazy import to avoid circular dependency
        from vnstock.explorer.fmarket.fund import Fund

        loop = asyncio.get_event_loop()

        # Initialize Fund with lazy loading
        fund = Fund()

        # Fetch asset allocation in executor to avoid blocking
        df = await loop.run_in_executor(
            None, lambda: fund.details.asset_holding(symbol=symbol.upper())
        )

        if df is None or df.empty:
            return f"No asset allocation data found for fund: {symbol}"

        # Convert to JSON
        return df.to_json(orient="records", date_format="iso", indent=2)

    except Exception as e:
        return f"Error fetching asset allocation for {symbol}: {str(e)}"


def main():
    """Main entry point for the MCP server."""
    if _use_http:
        # HTTP transport for remote deployment (Render, etc.)
        mcp.run(transport="streamable-http", host="0.0.0.0", port=PORT)
    else:
        # STDIO transport for local usage (uvx, Claude Desktop)
        mcp.run()


if __name__ == "__main__":
    main()

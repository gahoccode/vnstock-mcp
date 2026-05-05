"""Fund data service - handles fund listings, NAV reports, holdings, and allocations."""

from vnstock_mcp.config import VALID_FUND_TYPES
from vnstock_mcp.core.base import BaseService
from vnstock_mcp.models.fund import (
    FundAssetAllocationResult,
    FundHoldingsResult,
    FundIndustryAllocationResult,
    FundListingResult,
    FundNavResult,
    FundSearchResult,
)


class FundService(BaseService):
    """Service for fetching fund data."""

    async def get_fund_listing(
        self,
        fund_type: str = "",
    ) -> FundListingResult:
        """
        Get list of all available mutual funds.

        Args:
            fund_type: Filter by fund type - '' (all), 'BALANCED', 'BOND', 'STOCK'

        Returns:
            FundListingResult with DataFrame data or error
        """
        if fund_type not in VALID_FUND_TYPES:
            valid_types = ", ".join(sorted(VALID_FUND_TYPES))
            return FundListingResult.error_result(
                f"Invalid fund_type '{fund_type}'. Valid types: {valid_types}"
            )

        try:
            # Lazy import to avoid circular dependency
            from vnstock import Fund

            # Initialize Fund with lazy loading
            fund = Fund()

            # Fetch fund listing in executor to avoid blocking
            df = await self.run_sync(
                lambda: fund.listing(fund_type=fund_type)
            )

            if df is None or df.empty:
                return FundListingResult.empty_for_type(fund_type)

            return FundListingResult.success_result(df)

        except Exception as e:
            return FundListingResult.error_result(f"Error fetching fund listing: {e}")

    async def search_funds(
        self,
        symbol: str,
    ) -> FundSearchResult:
        """
        Search for mutual funds by symbol or partial name.

        Args:
            symbol: Fund short name or ticker (case-insensitive, partial match allowed)

        Returns:
            FundSearchResult with DataFrame data or error
        """
        try:
            # Lazy import to avoid circular dependency
            from vnstock import Fund

            # Initialize Fund with lazy loading
            fund = Fund()

            # Search for funds in executor to avoid blocking
            df = await self.run_sync(
                lambda: fund.filter(symbol=symbol)
            )

            if df is None or df.empty:
                return FundSearchResult.empty_for_symbol(symbol)

            return FundSearchResult.success_result(df)

        except Exception as e:
            return FundSearchResult.error_result(f"Error searching funds: {e}")

    async def get_fund_nav_report(
        self,
        symbol: str,
    ) -> FundNavResult:
        """
        Get historical NAV report for a specific mutual fund.

        Args:
            symbol: Fund short name/ticker (e.g., 'SSISCA', 'VESAF')

        Returns:
            FundNavResult with DataFrame data or error
        """
        try:
            # Lazy import to avoid circular dependency
            from vnstock import Fund

            # Initialize Fund with lazy loading
            fund = Fund()

            # Fetch NAV report in executor to avoid blocking
            df = await self.run_sync(
                lambda: fund.details.nav_report(symbol=symbol.upper())
            )

            if df is None or df.empty:
                return FundNavResult.empty_for_symbol(symbol)

            return FundNavResult.success_result(df)

        except Exception as e:
            return FundNavResult.error_result(
                f"Error fetching NAV report for {symbol}: {e}"
            )

    async def get_fund_top_holdings(
        self,
        symbol: str,
    ) -> FundHoldingsResult:
        """
        Get top 10 holdings for a specific mutual fund.

        Args:
            symbol: Fund short name/ticker (e.g., 'SSISCA', 'VESAF')

        Returns:
            FundHoldingsResult with DataFrame data or error
        """
        try:
            # Lazy import to avoid circular dependency
            from vnstock import Fund

            # Initialize Fund with lazy loading
            fund = Fund()

            # Fetch top holdings in executor to avoid blocking
            df = await self.run_sync(
                lambda: fund.details.top_holding(symbol=symbol.upper())
            )

            if df is None or df.empty:
                return FundHoldingsResult.empty_for_symbol(symbol)

            return FundHoldingsResult.success_result(df)

        except Exception as e:
            return FundHoldingsResult.error_result(
                f"Error fetching top holdings for {symbol}: {e}"
            )

    async def get_fund_industry_allocation(
        self,
        symbol: str,
    ) -> FundIndustryAllocationResult:
        """
        Get industry allocation breakdown for a specific mutual fund.

        Args:
            symbol: Fund short name/ticker (e.g., 'SSISCA', 'VESAF')

        Returns:
            FundIndustryAllocationResult with DataFrame data or error
        """
        try:
            # Lazy import to avoid circular dependency
            from vnstock import Fund

            # Initialize Fund with lazy loading
            fund = Fund()

            # Fetch industry allocation in executor to avoid blocking
            df = await self.run_sync(
                lambda: fund.details.industry_holding(symbol=symbol.upper())
            )

            if df is None or df.empty:
                return FundIndustryAllocationResult.empty_for_symbol(symbol)

            return FundIndustryAllocationResult.success_result(df)

        except Exception as e:
            return FundIndustryAllocationResult.error_result(
                f"Error fetching industry allocation for {symbol}: {e}"
            )

    async def get_fund_asset_allocation(
        self,
        symbol: str,
    ) -> FundAssetAllocationResult:
        """
        Get asset allocation breakdown for a specific mutual fund.

        Args:
            symbol: Fund short name/ticker (e.g., 'SSISCA', 'VESAF')

        Returns:
            FundAssetAllocationResult with DataFrame data or error
        """
        try:
            # Lazy import to avoid circular dependency
            from vnstock import Fund

            # Initialize Fund with lazy loading
            fund = Fund()

            # Fetch asset allocation in executor to avoid blocking
            df = await self.run_sync(
                lambda: fund.details.asset_holding(symbol=symbol.upper())
            )

            if df is None or df.empty:
                return FundAssetAllocationResult.empty_for_symbol(symbol)

            return FundAssetAllocationResult.success_result(df)

        except Exception as e:
            return FundAssetAllocationResult.error_result(
                f"Error fetching asset allocation for {symbol}: {e}"
            )

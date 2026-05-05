"""Result models for fund data."""

from vnstock_mcp.models.base import DataFrameResult


class FundListingResult(DataFrameResult):
    """Result for fund listing data."""

    @classmethod
    def empty_for_type(cls, fund_type: str) -> "FundListingResult":
        """Create empty result for a fund type."""
        return cls(
            success=False,
            error_message=f"No funds found for type: {fund_type}",
        )


class FundSearchResult(DataFrameResult):
    """Result for fund search data."""

    @classmethod
    def empty_for_symbol(cls, symbol: str) -> "FundSearchResult":
        """Create empty result for a fund symbol."""
        return cls(
            success=False,
            error_message=f"No funds found matching: {symbol}",
        )


class FundNavResult(DataFrameResult):
    """Result for fund NAV report data."""

    @classmethod
    def empty_for_symbol(cls, symbol: str) -> "FundNavResult":
        """Create empty result for a fund symbol."""
        return cls.empty_result("NAV", symbol)


class FundHoldingsResult(DataFrameResult):
    """Result for fund top holdings data."""

    @classmethod
    def empty_for_symbol(cls, symbol: str) -> "FundHoldingsResult":
        """Create empty result for a fund symbol."""
        return cls.empty_result("top holdings", symbol)


class FundIndustryAllocationResult(DataFrameResult):
    """Result for fund industry allocation data."""

    @classmethod
    def empty_for_symbol(cls, symbol: str) -> "FundIndustryAllocationResult":
        """Create empty result for a fund symbol."""
        return cls.empty_result("industry allocation", symbol)


class FundAssetAllocationResult(DataFrameResult):
    """Result for fund asset allocation data."""

    @classmethod
    def empty_for_symbol(cls, symbol: str) -> "FundAssetAllocationResult":
        """Create empty result for a fund symbol."""
        return cls.empty_result("asset allocation", symbol)

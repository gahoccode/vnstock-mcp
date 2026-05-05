"""Result models for company information."""

from vnstock_mcp.models.base import DataFrameResult


class CompanyInfoResult(DataFrameResult):
    """Result for company information data."""

    @classmethod
    def empty_for_symbol(cls, symbol: str, info_type: str) -> "CompanyInfoResult":
        """Create empty result for a stock symbol and info type."""
        return cls.empty_result(info_type, symbol)

"""Result models for financial data."""

from vnstock_mcp.models.base import DataFrameResult


class IncomeStatementResult(DataFrameResult):
    """Result for income statement data."""

    @classmethod
    def empty_for_symbol(cls, symbol: str) -> "IncomeStatementResult":
        """Create empty result for a stock symbol."""
        return cls.empty_result("income statement", symbol)


class BalanceSheetResult(DataFrameResult):
    """Result for balance sheet data."""

    @classmethod
    def empty_for_symbol(cls, symbol: str) -> "BalanceSheetResult":
        """Create empty result for a stock symbol."""
        return cls.empty_result("balance sheet", symbol)


class CashFlowResult(DataFrameResult):
    """Result for cash flow data."""

    @classmethod
    def empty_for_symbol(cls, symbol: str) -> "CashFlowResult":
        """Create empty result for a stock symbol."""
        return cls.empty_result("cash flow", symbol)


class FinancialRatiosResult(DataFrameResult):
    """Result for financial ratios data."""

    @classmethod
    def empty_for_symbol(cls, symbol: str) -> "FinancialRatiosResult":
        """Create empty result for a stock symbol."""
        return cls.empty_result("financial ratio", symbol)
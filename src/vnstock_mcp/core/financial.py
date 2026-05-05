"""Financial data service - handles income statements, balance sheets, cash flows, and ratios."""

from vnstock_mcp.core.base import BaseService
from vnstock_mcp.models.financial import (
    BalanceSheetResult,
    CashFlowResult,
    FinancialRatiosResult,
    IncomeStatementResult,
)
from vnstock_mcp.utils.data_transform import sort_financial_period_columns


class FinancialService(BaseService):
    """Service for fetching financial statement data."""

    async def get_income_statement(
        self,
        symbol: str,
    ) -> IncomeStatementResult:
        """
        Get annual income statement for a stock.

        Args:
            symbol: Stock ticker symbol (e.g., 'VCI', 'VNM', 'HPG')

        Returns:
            IncomeStatementResult with DataFrame data or error
        """
        try:
            # Lazy import to avoid circular dependency
            from vnstock import Finance

            finance = Finance(
                source="KBS",
                symbol=symbol.upper(),
                period="year",
                get_all=True,
                show_log=False,
            )

            # Fetch annual income statement in executor to avoid blocking
            df = await self.run_sync(
                lambda: finance.income_statement(period="year")
            )

            if df is None or df.empty:
                return IncomeStatementResult.empty_for_symbol(symbol)

            df = sort_financial_period_columns(df)

            return IncomeStatementResult.success_result(df)

        except Exception as e:
            return IncomeStatementResult.error_result(
                f"Error fetching income statement for {symbol}: {e}"
            )

    async def get_balance_sheet(
        self,
        symbol: str,
    ) -> BalanceSheetResult:
        """
        Get annual balance sheet for a stock.

        Args:
            symbol: Stock ticker symbol (e.g., 'VCI', 'VNM', 'HPG')

        Returns:
            BalanceSheetResult with DataFrame data or error
        """
        try:
            # Lazy import to avoid circular dependency
            from vnstock import Finance

            finance = Finance(
                source="KBS",
                symbol=symbol.upper(),
                period="year",
                get_all=True,
                show_log=False,
            )

            # Fetch annual balance sheet in executor to avoid blocking
            df = await self.run_sync(
                lambda: finance.balance_sheet(period="year")
            )

            if df is None or df.empty:
                return BalanceSheetResult.empty_for_symbol(symbol)

            df = sort_financial_period_columns(df)

            return BalanceSheetResult.success_result(df)

        except Exception as e:
            return BalanceSheetResult.error_result(
                f"Error fetching balance sheet for {symbol}: {e}"
            )

    async def get_cash_flow(
        self,
        symbol: str,
    ) -> CashFlowResult:
        """
        Get annual cash flow statement for a stock.

        Args:
            symbol: Stock ticker symbol (e.g., 'VCI', 'VNM', 'HPG')

        Returns:
            CashFlowResult with DataFrame data or error
        """
        try:
            # Lazy import to avoid circular dependency
            from vnstock import Finance

            finance = Finance(
                source="KBS",
                symbol=symbol.upper(),
                period="year",
                get_all=True,
                show_log=False,
            )

            # Fetch annual cash flow statement in executor to avoid blocking
            df = await self.run_sync(
                lambda: finance.cash_flow(period="year")
            )

            if df is None or df.empty:
                return CashFlowResult.empty_for_symbol(symbol)

            df = sort_financial_period_columns(df)

            return CashFlowResult.success_result(df)

        except Exception as e:
            return CashFlowResult.error_result(
                f"Error fetching cash flow for {symbol}: {e}"
            )

    async def get_financial_ratios(
        self,
        symbol: str,
    ) -> FinancialRatiosResult:
        """
        Get annual financial ratios for a stock.

        Args:
            symbol: Stock ticker symbol (e.g., 'VCI', 'VNM', 'HPG')

        Returns:
            FinancialRatiosResult with DataFrame data or error
        """
        try:
            # Lazy import to avoid circular dependency
            from vnstock import Finance

            finance = Finance(
                source="KBS",
                symbol=symbol.upper(),
                period="year",
                get_all=True,
                show_log=False,
            )

            # Fetch annual financial ratios in executor to avoid blocking
            df = await self.run_sync(
                lambda: finance.ratio(period="year")
            )

            if df is None or df.empty:
                return FinancialRatiosResult.empty_for_symbol(symbol)

            df = sort_financial_period_columns(df)

            return FinancialRatiosResult.success_result(df)

        except Exception as e:
            return FinancialRatiosResult.error_result(
                f"Error fetching financial ratios for {symbol}: {e}"
            )

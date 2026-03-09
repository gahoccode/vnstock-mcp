"""Financial data service - handles income statements, balance sheets, cash flows, and ratios."""

import asyncio

import pandas as pd

from vnstock_mcp.core.base import BaseService
from vnstock_mcp.models.financial import (
    BalanceSheetResult,
    CashFlowResult,
    FinancialRatiosResult,
    IncomeStatementResult,
)
from vnstock_mcp.utils.data_transform import sort_by_year


class FinancialService(BaseService):
    """Service for fetching financial statement data."""

    async def get_income_statement(
        self,
        symbol: str,
        lang: str = "en",
    ) -> IncomeStatementResult:
        """
        Get annual income statement for a stock.

        Args:
            symbol: Stock ticker symbol (e.g., 'VCI', 'VNM', 'HPG')
            lang: Language - 'en' (English) or 'vi' (Vietnamese)

        Returns:
            IncomeStatementResult with DataFrame data or error
        """
        try:
            # Lazy import to avoid circular dependency
            from vnstock.explorer.vci import Finance

            # Initialize Finance with VCI source
            finance = Finance(symbol=symbol.upper())

            # Fetch annual income statement in executor to avoid blocking
            df = await self.run_sync(
                lambda: finance.income_statement(period="year", lang=lang)
            )

            if df is None or df.empty:
                return IncomeStatementResult.empty_for_symbol(symbol)

            # Sort by yearReport for chronological analysis
            df = sort_by_year(df)

            return IncomeStatementResult.success_result(df)

        except Exception as e:
            return IncomeStatementResult.error_result(
                f"Error fetching income statement for {symbol}: {e}"
            )

    async def get_balance_sheet(
        self,
        symbol: str,
        lang: str = "en",
    ) -> BalanceSheetResult:
        """
        Get annual balance sheet for a stock.

        Args:
            symbol: Stock ticker symbol (e.g., 'VCI', 'VNM', 'HPG')
            lang: Language - 'en' (English) or 'vi' (Vietnamese)

        Returns:
            BalanceSheetResult with DataFrame data or error
        """
        try:
            # Lazy import to avoid circular dependency
            from vnstock.explorer.vci import Finance

            # Initialize Finance with VCI source
            finance = Finance(symbol=symbol.upper())

            # Fetch annual balance sheet in executor to avoid blocking
            df = await self.run_sync(
                lambda: finance.balance_sheet(period="year", lang=lang)
            )

            if df is None or df.empty:
                return BalanceSheetResult.empty_for_symbol(symbol)

            # Sort by yearReport for chronological analysis
            df = sort_by_year(df)

            return BalanceSheetResult.success_result(df)

        except Exception as e:
            return BalanceSheetResult.error_result(
                f"Error fetching balance sheet for {symbol}: {e}"
            )

    async def get_cash_flow(
        self,
        symbol: str,
        lang: str = "en",
    ) -> CashFlowResult:
        """
        Get annual cash flow statement for a stock.

        Args:
            symbol: Stock ticker symbol (e.g., 'VCI', 'VNM', 'HPG')
            lang: Language - 'en' (English) or 'vi' (Vietnamese)

        Returns:
            CashFlowResult with DataFrame data or error
        """
        try:
            # Lazy import to avoid circular dependency
            from vnstock.explorer.vci import Finance

            # Initialize Finance with VCI source
            finance = Finance(symbol=symbol.upper())

            # Fetch annual cash flow statement in executor to avoid blocking
            df = await self.run_sync(
                lambda: finance.cash_flow(period="year", lang=lang)
            )

            if df is None or df.empty:
                return CashFlowResult.empty_for_symbol(symbol)

            # Sort by yearReport for chronological analysis
            df = sort_by_year(df)

            return CashFlowResult.success_result(df)

        except Exception as e:
            return CashFlowResult.error_result(
                f"Error fetching cash flow for {symbol}: {e}"
            )

    async def get_financial_ratios(
        self,
        symbol: str,
        lang: str = "en",
    ) -> FinancialRatiosResult:
        """
        Get annual financial ratios for a stock.

        Args:
            symbol: Stock ticker symbol (e.g., 'VCI', 'VNM', 'HPG')
            lang: Language - 'en' (English) or 'vi' (Vietnamese)

        Returns:
            FinancialRatiosResult with DataFrame data or error
        """
        try:
            # Lazy imports to avoid circular dependency
            from vnstock.explorer.vci import Finance
            from vnstock.core.utils.transform import flatten_hierarchical_index

            loop = asyncio.get_event_loop()

            # Initialize Finance with VCI source
            finance = Finance(symbol=symbol.upper())

            # Fetch annual financial ratios in executor to avoid blocking
            df = await self.run_sync(
                lambda: finance.ratio(period="year", lang=lang)
            )

            if df is None or df.empty:
                return FinancialRatiosResult.empty_for_symbol(symbol)

            # Flatten MultiIndex DataFrame first, then sort chronologically
            flattened_df = await loop.run_in_executor(
                None,
                lambda: flatten_hierarchical_index(
                    df, separator="_", handle_duplicates=True, drop_levels=0
                ),
            )

            # Sort flattened DataFrame by yearReport for chronological analysis
            flattened_df = sort_by_year(flattened_df)

            return FinancialRatiosResult.success_result(flattened_df)

        except Exception as e:
            return FinancialRatiosResult.error_result(
                f"Error fetching financial ratios for {symbol}: {e}"
            )
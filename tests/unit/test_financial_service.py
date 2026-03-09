"""Unit tests for FinancialService."""

import pytest
from unittest.mock import MagicMock, patch
import pandas as pd

from vnstock_mcp.core.financial import FinancialService


@pytest.fixture
def financial_service():
    """Create a FinancialService instance."""
    return FinancialService()


@pytest.fixture
def sample_income_statement_df():
    """Create sample income statement DataFrame."""
    return pd.DataFrame({
        "yearReport": [2022, 2023, 2024],
        "revenue": [1000, 1100, 1200],
        "netProfit": [100, 110, 120],
    })


@pytest.fixture
def empty_df():
    """Create an empty DataFrame."""
    return pd.DataFrame()


class TestFinancialServiceGetIncomeStatement:
    """Tests for get_income_statement method."""

    @pytest.mark.asyncio
    async def test_success(self, financial_service, sample_income_statement_df):
        """Test successful income statement fetch."""
        mock_finance = MagicMock()
        mock_finance.income_statement.return_value = sample_income_statement_df

        with patch.dict(
            "sys.modules",
            {"vnstock.explorer.vci": MagicMock(Finance=MagicMock(return_value=mock_finance))}
        ):
            result = await financial_service.get_income_statement("VCI", "en")

            assert result.success
            assert result.data is not None
            assert len(result.data) == 3

    @pytest.mark.asyncio
    async def test_empty_data(self, financial_service, empty_df):
        """Test handling of empty data."""
        mock_finance = MagicMock()
        mock_finance.income_statement.return_value = empty_df

        with patch.dict(
            "sys.modules",
            {"vnstock.explorer.vci": MagicMock(Finance=MagicMock(return_value=mock_finance))}
        ):
            result = await financial_service.get_income_statement("INVALID", "en")

            assert not result.success
            assert "No income statement data found" in result.error_message

    @pytest.mark.asyncio
    async def test_none_data(self, financial_service):
        """Test handling of None data."""
        mock_finance = MagicMock()
        mock_finance.income_statement.return_value = None

        with patch.dict(
            "sys.modules",
            {"vnstock.explorer.vci": MagicMock(Finance=MagicMock(return_value=mock_finance))}
        ):
            result = await financial_service.get_income_statement("INVALID", "en")

            assert not result.success

    @pytest.mark.asyncio
    async def test_exception_handling(self, financial_service):
        """Test exception handling."""
        with patch.dict(
            "sys.modules",
            {"vnstock.explorer.vci": MagicMock(Finance=MagicMock(side_effect=Exception("API Error")))}
        ):
            result = await financial_service.get_income_statement("VCI", "en")

            assert not result.success
            assert "Error fetching income statement" in result.error_message

    @pytest.mark.asyncio
    async def test_symbol_uppercase(self, financial_service, sample_income_statement_df):
        """Test that symbol is converted to uppercase."""
        mock_finance = MagicMock()
        mock_finance.income_statement.return_value = sample_income_statement_df
        mock_finance_cls = MagicMock(return_value=mock_finance)

        with patch.dict(
            "sys.modules",
            {"vnstock.explorer.vci": MagicMock(Finance=mock_finance_cls)}
        ):
            await financial_service.get_income_statement("vci", "en")

            mock_finance_cls.assert_called_once_with(symbol="VCI")


class TestFinancialServiceGetBalanceSheet:
    """Tests for get_balance_sheet method."""

    @pytest.mark.asyncio
    async def test_success(self, financial_service):
        """Test successful balance sheet fetch."""
        df = pd.DataFrame({
            "yearReport": [2022, 2023],
            "totalAssets": [5000, 5500],
        })

        mock_finance = MagicMock()
        mock_finance.balance_sheet.return_value = df

        with patch.dict(
            "sys.modules",
            {"vnstock.explorer.vci": MagicMock(Finance=MagicMock(return_value=mock_finance))}
        ):
            result = await financial_service.get_balance_sheet("VCI", "en")

            assert result.success
            assert len(result.data) == 2


class TestFinancialServiceGetCashFlow:
    """Tests for get_cash_flow method."""

    @pytest.mark.asyncio
    async def test_success(self, financial_service):
        """Test successful cash flow fetch."""
        df = pd.DataFrame({
            "yearReport": [2022, 2023],
            "operatingCashFlow": [500, 600],
        })

        mock_finance = MagicMock()
        mock_finance.cash_flow.return_value = df

        with patch.dict(
            "sys.modules",
            {"vnstock.explorer.vci": MagicMock(Finance=MagicMock(return_value=mock_finance))}
        ):
            result = await financial_service.get_cash_flow("VCI", "en")

            assert result.success


class TestFinancialServiceGetFinancialRatios:
    """Tests for get_financial_ratios method."""

    @pytest.mark.asyncio
    async def test_success(self, financial_service):
        """Test successful financial ratios fetch."""
        # Create a DataFrame with MultiIndex columns
        df = pd.DataFrame({
            ("yearReport", ""): [2022, 2023],
            ("roe", "value"): [15.5, 16.2],
        })
        df.columns = pd.MultiIndex.from_tuples(df.columns)

        mock_finance = MagicMock()
        mock_finance.ratio.return_value = df

        flattened = pd.DataFrame({
            "yearReport": [2022, 2023],
            "roe_value": [15.5, 16.2],
        })

        with patch.dict(
            "sys.modules",
            {
                "vnstock.explorer.vci": MagicMock(Finance=MagicMock(return_value=mock_finance)),
                "vnstock.core.utils.transform": MagicMock(
                    flatten_hierarchical_index=MagicMock(return_value=flattened)
                ),
            }
        ):
            result = await financial_service.get_financial_ratios("VCI", "en")

            assert result.success
from unittest.mock import MagicMock, patch

import pandas as pd
import pytest

from vnstock_mcp.core.financial import FinancialService


@pytest.fixture
def financial_service():
    """Create a FinancialService instance."""
    return FinancialService()


@pytest.fixture
def sample_income_statement_df():
    """Create sample vnstock 4.x income statement DataFrame."""
    return pd.DataFrame({
        "item": ["Revenue", "Net profit"],
        "item_id": ["n_1.revenue", "n_20.net_profit"],
        "2023": [1100, 110],
        "2025": [1300, 130],
        "2024": [1200, 120],
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
            {"vnstock": MagicMock(Finance=MagicMock(return_value=mock_finance))}
        ):
            result = await financial_service.get_income_statement("VCI")

            assert result.success
            assert result.data is not None
            assert list(result.data.columns) == [
                "item",
                "item_id",
                "2025",
                "2024",
                "2023",
            ]

    @pytest.mark.asyncio
    async def test_empty_data(self, financial_service, empty_df):
        """Test handling of empty data."""
        mock_finance = MagicMock()
        mock_finance.income_statement.return_value = empty_df

        with patch.dict(
            "sys.modules",
            {"vnstock": MagicMock(Finance=MagicMock(return_value=mock_finance))}
        ):
            result = await financial_service.get_income_statement("INVALID")

            assert not result.success
            assert "No income statement data found" in result.error_message
            mock_finance.income_statement.assert_called_once_with(period="year")

    @pytest.mark.asyncio
    async def test_none_data(self, financial_service):
        """Test handling of None data."""
        mock_finance = MagicMock()
        mock_finance.income_statement.return_value = None

        with patch.dict(
            "sys.modules",
            {"vnstock": MagicMock(Finance=MagicMock(return_value=mock_finance))}
        ):
            result = await financial_service.get_income_statement("INVALID")

            assert not result.success

    @pytest.mark.asyncio
    async def test_exception_handling(self, financial_service):
        """Test exception handling."""
        with patch.dict(
            "sys.modules",
            {"vnstock": MagicMock(Finance=MagicMock(side_effect=Exception("API Error")))}
        ):
            result = await financial_service.get_income_statement("VCI")

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
            {"vnstock": MagicMock(Finance=mock_finance_cls)}
        ):
            await financial_service.get_income_statement("vci")

            mock_finance_cls.assert_called_once_with(
                source="KBS",
                symbol="VCI",
                period="year",
                get_all=True,
                show_log=False,
            )


class TestFinancialServiceGetBalanceSheet:
    """Tests for get_balance_sheet method."""

    @pytest.mark.asyncio
    async def test_success(self, financial_service):
        """Test successful balance sheet fetch."""
        df = pd.DataFrame({
            "item": ["Assets"],
            "item_id": ["assets"],
            "2024": [5500],
            "2025": [6000],
        })

        mock_finance = MagicMock()
        mock_finance.balance_sheet.return_value = df

        with patch.dict(
            "sys.modules",
            {"vnstock": MagicMock(Finance=MagicMock(return_value=mock_finance))}
        ):
            result = await financial_service.get_balance_sheet("VCI")

            assert result.success
            assert list(result.data.columns) == ["item", "item_id", "2025", "2024"]
            mock_finance.balance_sheet.assert_called_once_with(period="year")


class TestFinancialServiceGetCashFlow:
    """Tests for get_cash_flow method."""

    @pytest.mark.asyncio
    async def test_success(self, financial_service):
        """Test successful cash flow fetch."""
        df = pd.DataFrame({
            "item": ["Operating cash flow"],
            "item_id": ["i_cash_flows_from_operating_activities"],
            "2024": [600],
            "2025": [650],
        })

        mock_finance = MagicMock()
        mock_finance.cash_flow.return_value = df

        with patch.dict(
            "sys.modules",
            {"vnstock": MagicMock(Finance=MagicMock(return_value=mock_finance))}
        ):
            result = await financial_service.get_cash_flow("VCI")

            assert result.success
            mock_finance.cash_flow.assert_called_once_with(period="year")


class TestFinancialServiceGetFinancialRatios:
    """Tests for get_financial_ratios method."""

    @pytest.mark.asyncio
    async def test_success(self, financial_service):
        """Test successful financial ratios fetch."""
        df = pd.DataFrame({
            "item": ["ROE", "ROA"],
            "item_id": ["roe", "roa"],
            "2023": [15.5, 8.2],
            "2025": [17.0, 9.0],
            "2024": [16.2, 8.5],
        })

        mock_finance = MagicMock()
        mock_finance.ratio.return_value = df

        with patch.dict(
            "sys.modules",
            {"vnstock": MagicMock(Finance=MagicMock(return_value=mock_finance))}
        ):
            result = await financial_service.get_financial_ratios("VCI")

            assert result.success
            assert list(result.data.columns) == [
                "item",
                "item_id",
                "2025",
                "2024",
                "2023",
            ]
            mock_finance.ratio.assert_called_once_with(period="year")

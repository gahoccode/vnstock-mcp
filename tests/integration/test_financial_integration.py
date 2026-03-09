"""Integration tests for FinancialService with real API calls."""

import pytest

from vnstock_mcp.core.financial import FinancialService


@pytest.fixture
def financial_service():
    """Create a FinancialService instance."""
    return FinancialService()


@pytest.mark.integration
class TestFinancialServiceIntegration:
    """Integration tests for FinancialService with real vnstock API."""

    @pytest.mark.asyncio
    async def test_get_income_statement_real(self, financial_service):
        """Test getting real income statement data."""
        result = await financial_service.get_income_statement("VCI", "en")

        assert result.success
        assert result.data is not None
        assert len(result.data) > 0
        assert "yearReport" in result.data.columns

    @pytest.mark.asyncio
    async def test_get_balance_sheet_real(self, financial_service):
        """Test getting real balance sheet data."""
        result = await financial_service.get_balance_sheet("VNM", "en")

        assert result.success
        assert result.data is not None
        assert "yearReport" in result.data.columns

    @pytest.mark.asyncio
    async def test_get_cash_flow_real(self, financial_service):
        """Test getting real cash flow data."""
        result = await financial_service.get_cash_flow("HPG", "en")

        assert result.success
        assert result.data is not None

    @pytest.mark.asyncio
    async def test_get_financial_ratios_real(self, financial_service):
        """Test getting real financial ratios data."""
        result = await financial_service.get_financial_ratios("VCI", "en")

        assert result.success
        assert result.data is not None

    @pytest.mark.asyncio
    async def test_get_income_statement_vietnamese(self, financial_service):
        """Test getting income statement with Vietnamese language."""
        result = await financial_service.get_income_statement("VCI", "vi")

        assert result.success
        assert result.data is not None

    @pytest.mark.asyncio
    async def test_get_income_statement_invalid_symbol(self, financial_service):
        """Test getting income statement for invalid symbol."""
        result = await financial_service.get_income_statement("INVALID_SYMBOL_XYZ", "en")

        # Should return error result
        assert not result.success
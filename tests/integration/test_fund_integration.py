"""Integration tests for FundService with real API calls."""

import pytest

from vnstock_mcp.core.fund import FundService


@pytest.fixture
def fund_service():
    """Create a FundService instance."""
    return FundService()


@pytest.mark.integration
class TestFundServiceIntegration:
    """Integration tests for FundService with real vnstock API."""

    @pytest.mark.asyncio
    async def test_get_fund_listing_real(self, fund_service):
        """Test getting real fund listing."""
        result = await fund_service.get_fund_listing("")

        assert result.success
        assert result.data is not None
        assert len(result.data) > 0

    @pytest.mark.asyncio
    async def test_get_fund_listing_by_type_real(self, fund_service):
        """Test getting real fund listing filtered by type."""
        result = await fund_service.get_fund_listing("STOCK")

        assert result.success
        assert result.data is not None

    @pytest.mark.asyncio
    async def test_search_funds_real(self, fund_service):
        """Test searching for real funds."""
        result = await fund_service.search_funds("SSI")

        assert result.success
        assert result.data is not None

    @pytest.mark.asyncio
    async def test_get_fund_nav_report_real(self, fund_service):
        """Test getting real NAV report."""
        result = await fund_service.get_fund_nav_report("SSISCA")

        assert result.success
        assert result.data is not None

    @pytest.mark.asyncio
    async def test_get_fund_top_holdings_real(self, fund_service):
        """Test getting real top holdings."""
        result = await fund_service.get_fund_top_holdings("SSISCA")

        assert result.success
        assert result.data is not None

    @pytest.mark.asyncio
    async def test_get_fund_industry_allocation_real(self, fund_service):
        """Test getting real industry allocation."""
        result = await fund_service.get_fund_industry_allocation("SSISCA")

        assert result.success
        assert result.data is not None

    @pytest.mark.asyncio
    async def test_get_fund_asset_allocation_real(self, fund_service):
        """Test getting real asset allocation."""
        result = await fund_service.get_fund_asset_allocation("SSISCA")

        assert result.success
        assert result.data is not None

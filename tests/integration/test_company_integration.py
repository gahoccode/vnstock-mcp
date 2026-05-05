"""Integration tests for CompanyService with real API calls."""

import pytest

from vnstock_mcp.core.company import CompanyService


@pytest.fixture
def company_service():
    """Create a CompanyService instance."""
    return CompanyService()


@pytest.mark.integration
class TestCompanyServiceIntegration:
    """Integration tests for CompanyService with real vnstock API."""

    @pytest.mark.asyncio
    async def test_get_company_overview_real(self, company_service):
        """Test getting real company overview."""
        result = await company_service.get_company_info("VCI", "overview", "en")

        assert result.success
        assert result.data is not None

    @pytest.mark.asyncio
    async def test_get_company_shareholders_real(self, company_service):
        """Test getting real shareholders data."""
        result = await company_service.get_company_info("VNM", "shareholders", "en")

        assert result.success
        assert result.data is not None

    @pytest.mark.asyncio
    async def test_get_company_officers_real(self, company_service):
        """Test getting real officers data."""
        result = await company_service.get_company_info("HPG", "officers", "en")

        assert result.success
        assert result.data is not None

    @pytest.mark.asyncio
    async def test_get_company_events_real(self, company_service):
        """Test getting real company events."""
        result = await company_service.get_company_info("VCI", "events", "en")

        assert result.success
        assert result.data is not None

    @pytest.mark.asyncio
    async def test_get_company_news_real(self, company_service):
        """Test getting real company news."""
        result = await company_service.get_company_info("VNM", "news", "en")

        assert result.success
        assert result.data is not None

    @pytest.mark.asyncio
    async def test_get_company_trading_stats_real(self, company_service):
        """Test getting real trading statistics."""
        result = await company_service.get_company_info("HPG", "trading_stats", "en")

        assert result.success
        assert result.data is not None

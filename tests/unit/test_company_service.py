"""Unit tests for CompanyService."""

import pytest
from unittest.mock import MagicMock, patch
import pandas as pd

from vnstock_mcp.core.company import CompanyService


@pytest.fixture
def company_service():
    """Create a CompanyService instance."""
    return CompanyService()


@pytest.fixture
def sample_overview_df():
    """Create sample company overview DataFrame."""
    return pd.DataFrame({
        "ticker": ["VCI"],
        "companyName": ["Vietnam Construction and Import-Export"],
        "industry": ["Construction"],
    })


class TestCompanyServiceGetCompanyInfo:
    """Tests for get_company_info method."""

    @pytest.mark.asyncio
    async def test_overview_success(self, company_service, sample_overview_df):
        """Test successful company overview fetch."""
        mock_company = MagicMock()
        mock_company.overview.return_value = sample_overview_df

        with patch.dict(
            "sys.modules",
            {"vnstock.explorer.vci": MagicMock(Company=MagicMock(return_value=mock_company))}
        ):
            result = await company_service.get_company_info("VCI", "overview", "en")

            assert result.success
            assert result.data is not None

    @pytest.mark.asyncio
    async def test_shareholders_success(self, company_service):
        """Test successful shareholders fetch."""
        df = pd.DataFrame({
            "shareholderName": ["Shareholder A", "Shareholder B"],
            "ownershipPercent": [25.0, 15.0],
        })

        mock_company = MagicMock()
        mock_company.shareholders.return_value = df

        with patch.dict(
            "sys.modules",
            {"vnstock.explorer.vci": MagicMock(Company=MagicMock(return_value=mock_company))}
        ):
            result = await company_service.get_company_info("VCI", "shareholders", "en")

            assert result.success
            mock_company.shareholders.assert_called_once()

    @pytest.mark.asyncio
    async def test_officers_success(self, company_service):
        """Test successful officers fetch."""
        df = pd.DataFrame({
            "name": ["John Doe", "Jane Smith"],
            "position": ["CEO", "CFO"],
        })

        mock_company = MagicMock()
        mock_company.officers.return_value = df

        with patch.dict(
            "sys.modules",
            {"vnstock.explorer.vci": MagicMock(Company=MagicMock(return_value=mock_company))}
        ):
            result = await company_service.get_company_info("VCI", "officers", "en")

            assert result.success
            mock_company.officers.assert_called_once_with(filter_by="working")

    @pytest.mark.asyncio
    async def test_invalid_info_type(self, company_service):
        """Test handling of invalid info_type."""
        result = await company_service.get_company_info("VCI", "invalid_type", "en")

        assert not result.success
        assert "Invalid info_type" in result.error_message

    @pytest.mark.asyncio
    async def test_empty_data(self, company_service):
        """Test handling of empty data."""
        mock_company = MagicMock()
        mock_company.overview.return_value = pd.DataFrame()

        with patch.dict(
            "sys.modules",
            {"vnstock.explorer.vci": MagicMock(Company=MagicMock(return_value=mock_company))}
        ):
            result = await company_service.get_company_info("INVALID", "overview", "en")

            assert not result.success
            assert "No overview data found" in result.error_message

    @pytest.mark.asyncio
    async def test_exception_handling(self, company_service):
        """Test exception handling."""
        with patch.dict(
            "sys.modules",
            {"vnstock.explorer.vci": MagicMock(Company=MagicMock(side_effect=Exception("API Error")))}
        ):
            result = await company_service.get_company_info("VCI", "overview", "en")

            assert not result.success
            assert "Error fetching overview" in result.error_message

    @pytest.mark.asyncio
    async def test_all_info_types(self, company_service):
        """Test all info types are callable."""
        info_types = [
            "overview",
            "shareholders",
            "officers",
            "subsidiaries",
            "events",
            "news",
            "reports",
            "ratio_summary",
            "trading_stats",
        ]

        for info_type in info_types:
            mock_company = MagicMock()
            # Set up all methods to return a valid DataFrame
            for method in [
                "overview", "shareholders", "officers", "subsidiaries",
                "events", "news", "reports", "ratio_summary", "trading_stats"
            ]:
                getattr(mock_company, method).return_value = pd.DataFrame({"test": [1]})

            with patch.dict(
                "sys.modules",
                {"vnstock.explorer.vci": MagicMock(Company=MagicMock(return_value=mock_company))}
            ):
                result = await company_service.get_company_info("VCI", info_type, "en")

                assert result.success, f"Failed for info_type: {info_type}"
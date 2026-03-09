"""Unit tests for FundService."""

import pytest
from unittest.mock import MagicMock, patch
import pandas as pd

from vnstock_mcp.core.fund import FundService


@pytest.fixture
def fund_service():
    """Create a FundService instance."""
    return FundService()


@pytest.fixture
def sample_fund_listing_df():
    """Create sample fund listing DataFrame."""
    return pd.DataFrame({
        "shortName": ["SSISCA", "VESAF"],
        "fundType": ["STOCK", "STOCK"],
        "nav": [10000, 15000],
    })


class TestFundServiceGetFundListing:
    """Tests for get_fund_listing method."""

    @pytest.mark.asyncio
    async def test_success(self, fund_service, sample_fund_listing_df):
        """Test successful fund listing fetch."""
        mock_fund = MagicMock()
        mock_fund.listing.return_value = sample_fund_listing_df

        with patch.dict(
            "sys.modules",
            {"vnstock.explorer.fmarket.fund": MagicMock(Fund=MagicMock(return_value=mock_fund))}
        ):
            result = await fund_service.get_fund_listing("")

            assert result.success
            assert result.data is not None
            assert len(result.data) == 2

    @pytest.mark.asyncio
    async def test_with_type_filter(self, fund_service, sample_fund_listing_df):
        """Test fund listing with type filter."""
        mock_fund = MagicMock()
        mock_fund.listing.return_value = sample_fund_listing_df

        with patch.dict(
            "sys.modules",
            {"vnstock.explorer.fmarket.fund": MagicMock(Fund=MagicMock(return_value=mock_fund))}
        ):
            result = await fund_service.get_fund_listing("STOCK")

            assert result.success
            mock_fund.listing.assert_called_once_with(fund_type="STOCK")

    @pytest.mark.asyncio
    async def test_invalid_fund_type(self, fund_service):
        """Test handling of invalid fund type."""
        result = await fund_service.get_fund_listing("INVALID")

        assert not result.success
        assert "Invalid fund_type" in result.error_message

    @pytest.mark.asyncio
    async def test_empty_data(self, fund_service):
        """Test handling of empty data."""
        mock_fund = MagicMock()
        mock_fund.listing.return_value = pd.DataFrame()

        with patch.dict(
            "sys.modules",
            {"vnstock.explorer.fmarket.fund": MagicMock(Fund=MagicMock(return_value=mock_fund))}
        ):
            result = await fund_service.get_fund_listing("")

            assert not result.success
            assert "No funds found" in result.error_message


class TestFundServiceSearchFunds:
    """Tests for search_funds method."""

    @pytest.mark.asyncio
    async def test_success(self, fund_service):
        """Test successful fund search."""
        df = pd.DataFrame({
            "shortName": ["SSISCA", "SSI"],
            "fundId": [1, 2],
        })

        mock_fund = MagicMock()
        mock_fund.filter.return_value = df

        with patch.dict(
            "sys.modules",
            {"vnstock.explorer.fmarket.fund": MagicMock(Fund=MagicMock(return_value=mock_fund))}
        ):
            result = await fund_service.search_funds("SSI")

            assert result.success
            assert len(result.data) == 2

    @pytest.mark.asyncio
    async def test_no_results(self, fund_service):
        """Test handling of no results."""
        mock_fund = MagicMock()
        mock_fund.filter.return_value = pd.DataFrame()

        with patch.dict(
            "sys.modules",
            {"vnstock.explorer.fmarket.fund": MagicMock(Fund=MagicMock(return_value=mock_fund))}
        ):
            result = await fund_service.search_funds("NOTFOUND")

            assert not result.success
            assert "No funds found matching" in result.error_message


class TestFundServiceGetFundNavReport:
    """Tests for get_fund_nav_report method."""

    @pytest.mark.asyncio
    async def test_success(self, fund_service):
        """Test successful NAV report fetch."""
        df = pd.DataFrame({
            "date": ["2024-01-01", "2024-01-02"],
            "nav": [10000, 10100],
        })

        mock_fund = MagicMock()
        mock_fund.details.nav_report.return_value = df

        with patch.dict(
            "sys.modules",
            {"vnstock.explorer.fmarket.fund": MagicMock(Fund=MagicMock(return_value=mock_fund))}
        ):
            result = await fund_service.get_fund_nav_report("SSISCA")

            assert result.success
            mock_fund.details.nav_report.assert_called_once_with(symbol="SSISCA")

    @pytest.mark.asyncio
    async def test_symbol_uppercase(self, fund_service):
        """Test that symbol is converted to uppercase."""
        mock_fund = MagicMock()
        mock_fund.details.nav_report.return_value = pd.DataFrame({"test": [1]})

        with patch.dict(
            "sys.modules",
            {"vnstock.explorer.fmarket.fund": MagicMock(Fund=MagicMock(return_value=mock_fund))}
        ):
            await fund_service.get_fund_nav_report("ssisca")

            mock_fund.details.nav_report.assert_called_once_with(symbol="SSISCA")


class TestFundServiceGetFundTopHoldings:
    """Tests for get_fund_top_holdings method."""

    @pytest.mark.asyncio
    async def test_success(self, fund_service):
        """Test successful top holdings fetch."""
        df = pd.DataFrame({
            "stockCode": ["VNM", "HPG", "FPT"],
            "netAssetPercent": [10.0, 8.0, 6.0],
        })

        mock_fund = MagicMock()
        mock_fund.details.top_holding.return_value = df

        with patch.dict(
            "sys.modules",
            {"vnstock.explorer.fmarket.fund": MagicMock(Fund=MagicMock(return_value=mock_fund))}
        ):
            result = await fund_service.get_fund_top_holdings("SSISCA")

            assert result.success
            assert len(result.data) == 3


class TestFundServiceGetFundIndustryAllocation:
    """Tests for get_fund_industry_allocation method."""

    @pytest.mark.asyncio
    async def test_success(self, fund_service):
        """Test successful industry allocation fetch."""
        df = pd.DataFrame({
            "industry": ["Banking", "Real Estate", "Technology"],
            "netAssetPercent": [30.0, 25.0, 20.0],
        })

        mock_fund = MagicMock()
        mock_fund.details.industry_holding.return_value = df

        with patch.dict(
            "sys.modules",
            {"vnstock.explorer.fmarket.fund": MagicMock(Fund=MagicMock(return_value=mock_fund))}
        ):
            result = await fund_service.get_fund_industry_allocation("SSISCA")

            assert result.success


class TestFundServiceGetFundAssetAllocation:
    """Tests for get_fund_asset_allocation method."""

    @pytest.mark.asyncio
    async def test_success(self, fund_service):
        """Test successful asset allocation fetch."""
        df = pd.DataFrame({
            "assetType": ["Stocks", "Bonds", "Cash"],
            "percent": [70.0, 20.0, 10.0],
        })

        mock_fund = MagicMock()
        mock_fund.details.asset_holding.return_value = df

        with patch.dict(
            "sys.modules",
            {"vnstock.explorer.fmarket.fund": MagicMock(Fund=MagicMock(return_value=mock_fund))}
        ):
            result = await fund_service.get_fund_asset_allocation("SSISCA")

            assert result.success
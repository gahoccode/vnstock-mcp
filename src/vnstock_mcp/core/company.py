"""Company information service - handles company overview, shareholders, officers, etc."""

from vnstock_mcp.config import VALID_INFO_TYPES
from vnstock_mcp.core.base import BaseService
from vnstock_mcp.models.company import CompanyInfoResult


class CompanyService(BaseService):
    """Service for fetching company information."""

    async def get_company_info(
        self,
        symbol: str,
        info_type: str = "overview",
        lang: str = "en",
    ) -> CompanyInfoResult:
        """
        Get company information for a stock.

        Args:
            symbol: Stock ticker symbol (e.g., 'VCI', 'ACB', 'HPG')
            info_type: Type of company information to fetch:
                      'overview' - Company overview and basic information
                      'shareholders' - Major shareholders information
                      'officers' - Company officers and management
                      'subsidiaries' - Subsidiaries and associated companies
                      'events' - Corporate events and announcements
                      'news' - Company news and updates
                      'reports' - Analysis reports
                      'ratio_summary' - Financial ratios summary
                      'trading_stats' - Trading statistics and market data
            lang: Language - 'en' (English) or 'vi' (Vietnamese)

        Returns:
            CompanyInfoResult with DataFrame data or error
        """
        # Validate info_type
        if info_type not in VALID_INFO_TYPES:
            valid_types = ", ".join(sorted(VALID_INFO_TYPES))
            return CompanyInfoResult.error_result(
                f"Invalid info_type '{info_type}'. Valid types: {valid_types}"
            )

        try:
            # Lazy import to avoid circular dependency
            from vnstock.explorer.vci import Company

            # Initialize Company with VCI source
            company = Company(symbol=symbol.upper())

            # Fetch the requested company information
            df = await self._fetch_by_info_type(company, info_type)

            if df is None or df.empty:
                return CompanyInfoResult.empty_for_symbol(symbol, info_type)

            return CompanyInfoResult.success_result(df)

        except Exception as e:
            return CompanyInfoResult.error_result(
                f"Error fetching {info_type} for {symbol}: {e}"
            )

    async def _fetch_by_info_type(self, company, info_type: str):
        """Fetch data by info type using the appropriate Company method."""
        fetch_methods = {
            "overview": lambda: company.overview(),
            "shareholders": lambda: company.shareholders(),
            "officers": lambda: company.officers(filter_by="working"),
            "subsidiaries": lambda: company.subsidiaries(filter_by="all"),
            "events": lambda: company.events(),
            "news": lambda: company.news(),
            "reports": lambda: company.reports(),
            "ratio_summary": lambda: company.ratio_summary(),
            "trading_stats": lambda: company.trading_stats(),
        }

        method = fetch_methods.get(info_type)
        if method:
            return await self.run_sync(method)
        return None
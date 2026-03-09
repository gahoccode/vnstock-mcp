"""Custom exceptions for VNStock MCP Server."""


class VnstockMCPError(Exception):
    """Base exception for all VNStock MCP errors."""

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(self.message)


class DataNotFoundError(VnstockMCPError):
    """Raised when requested data is not found."""

    def __init__(self, resource: str, identifier: str) -> None:
        message = f"No {resource} data found for {identifier}"
        super().__init__(message)
        self.resource = resource
        self.identifier = identifier


class InvalidParameterError(VnstockMCPError):
    """Raised when an invalid parameter is provided."""

    def __init__(
        self,
        parameter: str,
        value: str,
        valid_values: frozenset[str] | None = None,
    ) -> None:
        if valid_values:
            message = (
                f"Invalid {parameter} '{value}'. "
                f"Valid values: {', '.join(sorted(valid_values))}"
            )
        else:
            message = f"Invalid {parameter}: {value}"
        super().__init__(message)
        self.parameter = parameter
        self.value = value
        self.valid_values = valid_values


class DataFetchError(VnstockMCPError):
    """Raised when data fetch from vnstock fails."""

    def __init__(self, resource: str, identifier: str, original_error: str) -> None:
        message = f"Error fetching {resource} for {identifier}: {original_error}"
        super().__init__(message)
        self.resource = resource
        self.identifier = identifier
        self.original_error = original_error
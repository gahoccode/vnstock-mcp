"""Base result classes for service responses."""

from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar

import pandas as pd

T = TypeVar("T")


class ServiceResult(ABC, Generic[T]):
    """
    Abstract base class for service results.

    Provides a consistent interface for handling success/failure
    and converting results to JSON strings for MCP tools.
    """

    def __init__(
        self,
        success: bool,
        data: T | None = None,
        error_message: str | None = None,
    ) -> None:
        self.success = success
        self.data = data
        self.error_message = error_message

    @abstractmethod
    def to_json(self) -> str:
        """Convert result to JSON string for MCP tool response."""
        pass


class DataFrameResult(ServiceResult[pd.DataFrame]):
    """Result class for DataFrame responses."""

    def __init__(
        self,
        success: bool,
        data: pd.DataFrame | None = None,
        error_message: str | None = None,
        orient: str = "records",
        date_format: str = "iso",
        indent: int = 2,
    ) -> None:
        super().__init__(success, data, error_message)
        self.orient = orient
        self.date_format = date_format
        self.indent = indent

    def to_json(self) -> str:
        """Convert DataFrame to JSON string."""
        if not self.success:
            return self.error_message or "Unknown error"

        if self.data is None or self.data.empty:
            return self.error_message or "No data available"

        return self.data.to_json(
            orient=self.orient,
            date_format=self.date_format,
            indent=self.indent,
        )

    @classmethod
    def success_result(
        cls,
        data: pd.DataFrame,
        orient: str = "records",
        date_format: str = "iso",
        indent: int = 2,
    ) -> "DataFrameResult":
        """Create a successful DataFrame result."""
        return cls(
            success=True,
            data=data,
            orient=orient,
            date_format=date_format,
            indent=indent,
        )

    @classmethod
    def error_result(cls, error_message: str) -> "DataFrameResult":
        """Create an error DataFrame result."""
        return cls(success=False, error_message=error_message)

    @classmethod
    def empty_result(cls, resource: str, identifier: str) -> "DataFrameResult":
        """Create an empty DataFrame result with appropriate message."""
        return cls(
            success=False,
            error_message=f"No {resource} data found for {identifier}",
        )
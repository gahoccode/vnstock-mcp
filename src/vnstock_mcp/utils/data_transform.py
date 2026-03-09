"""DataFrame transformation utilities."""

from typing import Any

import pandas as pd


def sort_by_year(df: pd.DataFrame, year_column: str = "yearReport") -> pd.DataFrame:
    """
    Sort DataFrame by year column for chronological analysis.

    Args:
        df: DataFrame to sort
        year_column: Name of the year column to sort by

    Returns:
        Sorted DataFrame with reset index
    """
    if year_column in df.columns:
        return df.sort_values(year_column).reset_index(drop=True)
    return df


def dataframe_to_json(
    df: pd.DataFrame | None,
    orient: str = "records",
    date_format: str = "iso",
    indent: int = 2,
) -> str:
    """
    Convert DataFrame to JSON string.

    Args:
        df: DataFrame to convert
        orient: JSON orientation
        date_format: Date format for datetime columns
        indent: JSON indentation

    Returns:
        JSON string representation of the DataFrame
    """
    if df is None or df.empty:
        return ""
    return df.to_json(orient=orient, date_format=date_format, indent=indent)


def flatten_dataframe(
    df: pd.DataFrame,
    separator: str = "_",
    handle_duplicates: bool = True,
    drop_levels: int = 0,
) -> pd.DataFrame:
    """
    Flatten a MultiIndex DataFrame to single-level columns.

    Args:
        df: DataFrame with potentially MultiIndex columns
        separator: Separator for joined column names
        handle_duplicates: Whether to handle duplicate column names
        drop_levels: Number of levels to drop from MultiIndex

    Returns:
        DataFrame with flattened column names
    """
    if not isinstance(df.columns, pd.MultiIndex):
        return df

    from vnstock.core.utils.transform import flatten_hierarchical_index

    return flatten_hierarchical_index(
        df,
        separator=separator,
        handle_duplicates=handle_duplicates,
        drop_levels=drop_levels,
    )


def safe_to_json_string(
    df: pd.DataFrame | None,
    error_message: str,
) -> str:
    """
    Safely convert DataFrame to JSON, returning error message if empty.

    Args:
        df: DataFrame to convert
        error_message: Message to return if DataFrame is empty

    Returns:
        JSON string or error message
    """
    if df is None or df.empty:
        return error_message
    return dataframe_to_json(df)
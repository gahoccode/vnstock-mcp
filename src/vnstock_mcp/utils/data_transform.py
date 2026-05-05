"""DataFrame transformation utilities."""

import pandas as pd


def sort_financial_period_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Order vnstock 4.x financial period columns with metadata first.

    Args:
        df: Financial statement or ratio DataFrame

    Returns:
        DataFrame with metadata columns first and period columns descending
    """
    if df.empty:
        return df

    metadata_columns = [
        column for column in ["item", "item_en", "item_id"] if column in df.columns
    ]
    period_columns = sorted(
        [
            column
            for column in df.columns
            if isinstance(column, str) and column.isdigit()
        ],
        reverse=True,
    )
    remaining_columns = [
        column
        for column in df.columns
        if column not in metadata_columns and column not in period_columns
    ]

    return df[metadata_columns + period_columns + remaining_columns]


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

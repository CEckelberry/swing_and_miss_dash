import pandas as pd


def format_decimal_columns(df, columns, precision=3):
    """
    Formats specified columns of a DataFrame to have a given precision
    with trailing zeros, ensuring they remain as float types for compatibility.
    Additionally, converts percentage columns to percentage format.
    """
    for column in columns:
        if column in df.columns:
            if column in ["K%", "BB%"]:  # Convert to percentage format
                df[column] = df[column].apply(
                    lambda x: f"{x*100:.2f}%" if not pd.isna(x) else x
                )
            else:
                df[column] = df[column].apply(
                    lambda x: f"{x:.{precision}f}" if not pd.isna(x) else x
                )
    return df

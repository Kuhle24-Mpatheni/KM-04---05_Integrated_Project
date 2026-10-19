
"""
data_cleaning.py
Load and clean product and sales CSV files.
"""

import pandas as pd


def load_raw_data(products_path: str, sales_path: str):
    """Load the raw product and sales CSV files."""
    products_df = pd.read_csv(products_path)
    sales_df = pd.read_csv(sales_path)
    return products_df, sales_df


def clean_products(products_df: "pd.DataFrame") -> "pd.DataFrame":
    """Return a cleaned copy of the products DataFrame."""
    products = products_df.copy()

    # Remove extra spaces from text columns.
    for column in ["product_id", "product_name", "category"]:
        products[column] = products[column].apply(
            lambda value: value.strip() if isinstance(value, str) else value
        )

    # Convert prices to numeric values.
    products["unit_price"] = pd.to_numeric(
        products["unit_price"], errors="coerce"
    )

    # Remove products without a usable ID, name, or price.
    products = products.dropna(
        subset=["product_id", "product_name", "unit_price"]
    )
    products = products[
        products["product_id"].ne("")
        & products["product_name"].ne("")
    ]

    # Remove exact duplicate rows.
    products = products.drop_duplicates()

    # Standardise category capitalisation.
    products["category"] = products["category"].apply(
        lambda value: value.title() if isinstance(value, str) else value
    )

    return products.reset_index(drop=True)


def clean_sales(
    sales_df: "pd.DataFrame", valid_product_ids
) -> "pd.DataFrame":
    """Clean sales records and standardise their dates."""
    sales = sales_df.copy()

    # Remove exact duplicate rows.
    sales = sales.drop_duplicates()

    # Parse dates using the formats found in the supplied CSV.
    date_formats = [
        "%Y-%m-%d",
        "%d/%m/%Y",
        "%Y/%m/%d",
        "%d-%m-%Y",
    ]

    original_dates = sales["sale_date"].astype("string").str.strip()
    parsed_dates = pd.Series(
        pd.NaT, index=sales.index, dtype="datetime64[ns]"
    )

    for date_format in date_formats:
        remaining = parsed_dates.isna() & original_dates.notna()
        parsed_dates.loc[remaining] = pd.to_datetime(
            original_dates.loc[remaining],
            format=date_format,
            errors="coerce",
        )

    sales["sale_date"] = parsed_dates

    # Remove records without a usable date or quantity.
    sales = sales.dropna(subset=["sale_date", "quantity"])

    # Ensure quantities are numeric and positive.
    sales["quantity"] = pd.to_numeric(
        sales["quantity"], errors="coerce"
    )
    sales = sales.dropna(subset=["quantity"])
    sales = sales[sales["quantity"] > 0]

    # Remove sales that reference products not in the cleaned table.
    sales = sales[sales["product_id"].isin(valid_product_ids)]

    # Use Unknown when the payment method is missing or blank.
    sales["payment_method"] = (
        sales["payment_method"]
        .fillna("Unknown")
        .astype(str)
        .str.strip()
        .replace("", "Unknown")
    )

    # Store all valid dates in YYYY-MM-DD format.
    sales["sale_date"] = sales["sale_date"].dt.strftime("%Y-%m-%d")

    return sales.reset_index(drop=True)


def cleaning_summary(
    raw_df: "pd.DataFrame",
    clean_df: "pd.DataFrame",
    name: str,
) -> str:
    """Summarise the number of rows before and after cleaning."""
    raw_count = len(raw_df)
    clean_count = len(clean_df)
    removed_count = raw_count - clean_count

    return (
        f"{name}: {raw_count} raw rows -> "
        f"{clean_count} clean rows ({removed_count} removed)"
    )

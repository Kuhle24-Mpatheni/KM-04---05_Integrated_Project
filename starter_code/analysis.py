
"""
analysis.py
Plain-Python analysis for the spaza shop sales project.
"""


def total_sales_records(sales_rows: list) -> int:
    """Count sales records using a loop."""
    count = 0

    for row in sales_rows:
        count += 1

    return count


def low_stock_alert(products_rows: list, threshold: int = 5) -> list:
    """Return products that are out of stock."""
    alerts = []

    for product in products_rows:
        in_stock = product.get("in_stock", True)

        if in_stock is False or str(in_stock).strip().lower() == "false":
            alerts.append(product["product_name"])

    return alerts


def monthly_sales_trend(sales_rows: list) -> dict:
    """Calculate total units sold for each month."""
    trend = {}

    for row in sales_rows:
        sale_date = row.get("sale_date")
        quantity = row.get("quantity")

        if sale_date and quantity is not None:
            month = str(sale_date)[:7]

            if month in trend:
                trend[month] += int(quantity)
            else:
                trend[month] = int(quantity)

    return dict(sorted(trend.items()))


def classify_transaction_size(quantity: int) -> str:
    """Classify a transaction by the quantity sold."""
    if quantity >= 5:
        return "Bulk"
    elif quantity >= 2:
        return "Multiple"
    elif quantity == 1:
        return "Single"
    else:
        return "Invalid"


def average_basket_size(sales_rows: list) -> float:
    """Calculate average units per sale."""
    if not sales_rows:
        return 0.0

    total = 0

    for row in sales_rows:
        total += int(row["quantity"])

    return round(total / len(sales_rows), 2)

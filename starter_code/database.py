
"""
database.py
Create and query the SQLite database for the spaza shop project.
"""

import sqlite3


def get_connection(db_path: str = "store.db") -> sqlite3.Connection:
    """Open or create the SQLite database."""
    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def create_tables(conn: sqlite3.Connection) -> None:
    """Create the products and sales tables."""
    conn.execute("""
        CREATE TABLE IF NOT EXISTS products (
            product_id TEXT PRIMARY KEY,
            product_name TEXT NOT NULL,
            category TEXT,
            unit_price REAL
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS sales (
            sale_id TEXT PRIMARY KEY,
            product_id TEXT,
            quantity INTEGER,
            sale_date TEXT,
            payment_method TEXT,
            customer_type TEXT,
            FOREIGN KEY (product_id) REFERENCES products(product_id)
        )
    """)

    conn.commit()


def insert_products(conn: sqlite3.Connection, products_df) -> None:
    """Insert cleaned products into the database."""
    rows = products_df[
        ["product_id", "product_name", "category", "unit_price"]
    ].itertuples(index=False, name=None)

    conn.executemany("""
        INSERT OR REPLACE INTO products
        (product_id, product_name, category, unit_price)
        VALUES (?, ?, ?, ?)
    """, rows)

    conn.commit()


def insert_sales(conn: sqlite3.Connection, sales_df) -> None:
    """Insert cleaned sales into the database."""
    rows = sales_df[
        [
            "sale_id", "product_id", "quantity", "sale_date",
            "payment_method", "customer_type"
        ]
    ].itertuples(index=False, name=None)

    conn.executemany("""
        INSERT OR REPLACE INTO sales
        (sale_id, product_id, quantity, sale_date,
         payment_method, customer_type)
        VALUES (?, ?, ?, ?, ?, ?)
    """, rows)

    conn.commit()


def query_total_revenue_per_product(conn: sqlite3.Connection):
    """Which products generate the most revenue?"""
    sql = """
        SELECT p.product_name,
               SUM(s.quantity * p.unit_price) AS total_revenue
        FROM sales AS s
        JOIN products AS p ON s.product_id = p.product_id
        GROUP BY p.product_id, p.product_name
        ORDER BY total_revenue DESC
    """
    return conn.execute(sql).fetchall()


def query_best_selling_product(conn: sqlite3.Connection):
    """Which product has the highest total quantity sold?"""
    sql = """
        SELECT p.product_name, SUM(s.quantity) AS quantity_sold
        FROM sales AS s
        JOIN products AS p ON s.product_id = p.product_id
        GROUP BY p.product_id, p.product_name
        ORDER BY quantity_sold DESC
        LIMIT 1
    """
    return conn.execute(sql).fetchall()


def query_sales_by_payment_method(conn: sqlite3.Connection):
    """How many transactions used each payment method?"""
    sql = """
        SELECT payment_method, COUNT(*) AS transaction_count
        FROM sales
        GROUP BY payment_method
        ORDER BY transaction_count DESC
    """
    return conn.execute(sql).fetchall()


def query_custom_one(conn: sqlite3.Connection):
    """Which product category generates the most revenue?"""
    sql = """
        SELECT p.category,
               SUM(s.quantity * p.unit_price) AS total_revenue
        FROM sales AS s
        JOIN products AS p ON s.product_id = p.product_id
        GROUP BY p.category
        ORDER BY total_revenue DESC
    """
    return conn.execute(sql).fetchall()


def query_custom_two(conn: sqlite3.Connection):
    """How many units were sold in each month?"""
    sql = """
        SELECT substr(sale_date, 1, 7) AS sale_month,
               SUM(quantity) AS units_sold
        FROM sales
        WHERE sale_date IS NOT NULL
        GROUP BY substr(sale_date, 1, 7)
        ORDER BY sale_month
    """
    return conn.execute(sql).fetchall()

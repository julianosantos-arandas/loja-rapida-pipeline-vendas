import sqlite3

import pandas as pd

from src.pipelines.pipeline_vendas import ensure_db_schema


def test_ensure_db_schema_creates_vendas_table():
    conn = sqlite3.connect(":memory:")

    ensure_db_schema(conn)

    cursor = conn.cursor()
    cursor.execute("""
        SELECT name
        FROM sqlite_master
        WHERE type='table' AND name='vendas';
    """)

    table = cursor.fetchone()

    conn.close()

    assert table is not None

def test_insert_and_count_rows_in_vendas():
    conn = sqlite3.connect(":memory:")
    ensure_db_schema(conn)

    df = pd.DataFrame({
    "order_id": [1],
    "product_id": [1001],
    "product_name": ["Panela 20cm"],
    "order_date": ["2024-11-01"],
    "order_time": ["10:00"],
    "quantity": [2],
    "unit_price": [10.0],
    "discount_pct": [0.1],
    "order_status": ["paid"],
    "customer_id": ["C001"],
})


    df.to_sql("vendas", conn, if_exists="append", index=False)

    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM vendas")
    count = cursor.fetchone()[0]

    conn.close()

    assert count == 1

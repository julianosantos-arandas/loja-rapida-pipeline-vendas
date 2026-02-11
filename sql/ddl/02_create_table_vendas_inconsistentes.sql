CREATE TABLE IF NOT EXISTS vendas_inconsistentes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    order_id INTEGER,
    order_date TEXT,
    order_time TEXT,
    customer_id TEXT,
    customer_city TEXT,
    product_id TEXT,
    product_name TEXT,
    category TEXT,
    quantity INTEGER,
    unit_price REAL,
    discount_pct REAL,
    payment_method TEXT,
    channel TEXT,
    order_status TEXT
);

CREATE TABLE IF NOT EXISTS vendas (
    order_id INTEGER NOT NULL,
    order_date TEXT NOT NULL, 
    order_time TEXT,
    customer_id TEXT NOT NULL,
    customer_city TEXT,
    product_id TEXT NOT NULL,
    product_name TEXT NOT NULL,
    category TEXT,
    quantity INTEGER NOT NULL,
    unit_price REAL NOT NULL,
    discount_pct REAL,
    payment_method TEXT,
    channel TEXT, 
    order_status TEXT NOT NULL,

    PRIMARY KEY (order_id, product_id)
);

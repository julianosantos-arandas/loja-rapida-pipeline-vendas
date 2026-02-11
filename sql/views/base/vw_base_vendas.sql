DROP VIEW IF EXISTS vw_base_vendas;

CREATE VIEW vw_base_vendas AS
SELECT
    order_id,
    order_date,
    order_time,
    strftime('%Y-%m', order_date) AS ano_mes,
    CAST(strftime('%H', order_time) AS INTEGER) AS hora_pedido,

    customer_city,
    product_name,
    order_status,
    quantity,
    category,
    unit_price,
    discount_pct,

    ROUND(
    quantity * unit_price * (1 - COALESCE(discount_pct, 0)),
    2
) AS valor_linha_total_rs

FROM vendas;

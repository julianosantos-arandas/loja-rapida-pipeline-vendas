SELECT
    ROUND(
        SUM(quantity * unit_price * (1 - COALESCE(discount_pct, 0))),
        2
    )AS receita_cancelled

FROM vendas
WHERE order_status = 'cancelled';
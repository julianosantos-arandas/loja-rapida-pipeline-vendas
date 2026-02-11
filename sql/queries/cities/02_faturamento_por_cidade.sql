-- Faturamento por cidade (somente vendas pagas)
SELECT
    customer_city,
    ROUND(
    SUM(quantity * unit_price * (1 - COALESCE(discount_pct, 0))),
    2
    ) AS faturamento_paid
FROM vendas
WHERE order_status = 'paid'
GROUP BY customer_city
ORDER BY faturamento_paid DESC;

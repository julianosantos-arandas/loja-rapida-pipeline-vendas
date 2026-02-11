DROP VIEW IF EXISTS vw_analytics_faturamento_por_cidades;
CREATE VIEW vw_analytics_faturamento_por_cidades AS
SELECT
    customer_city,
    ROUND(
    SUM(quantity * unit_price * (1 - COALESCE(discount_pct, 0))),
    2
    ) AS faturamento_paid
FROM vw_base_vendas
WHERE order_status = 'paid'
GROUP BY customer_city
ORDER BY faturamento_paid DESC;

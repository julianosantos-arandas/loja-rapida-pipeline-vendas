DROP VIEW IF EXISTS vw_analytics_faturamento_mensal;

CREATE VIEW vw_analytics_faturamento_mensal AS
SELECT
    strftime('%Y-%m', order_date) AS ano_mes,
    ROUND(SUM(quantity * unit_price * (1 - COALESCE(discount_pct, 0))),2)AS faturamento_total,
    COUNT(DISTINCT order_id) AS total_pedidos
FROM vw_base_vendas
WHERE order_status IN ('paid')
GROUP BY ano_mes
ORDER BY ano_mes;




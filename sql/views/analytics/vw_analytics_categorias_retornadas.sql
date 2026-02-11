DROP VIEW IF EXISTS vw_analytics_categorias_retornadas;
CREATE VIEW vw_analytics_categorias_retornadas AS
SELECT
    category,
    ROUND(SUM(quantity * unit_price * (1 - COALESCE(discount_pct, 0))),2)AS total_de_vendas_retornadas

FROM vw_base_vendas
WHERE order_status = 'returned'
GROUP BY category
ORDER BY total_de_vendas_retornadas DESC;
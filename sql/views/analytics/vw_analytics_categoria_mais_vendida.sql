DROP VIEW IF EXISTS vw_analytics_categoria_mais_vendida;
CREATE VIEW vw_analytics_categoria_mais_vendida AS
SELECT
    category,
    ROUND(SUM(quantity * unit_price * (1 - COALESCE(discount_pct, 0))),2) AS total_de_vendas

FROM vw_base_vendas_financeiras
WHERE order_status = 'paid'
GROUP BY category
ORDER BY total_de_vendas DESC;
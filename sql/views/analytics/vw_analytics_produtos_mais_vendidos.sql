DROP VIEW IF EXISTS vw_analytics_produtos_mais_vendidos;
CREATE VIEW vw_analytics_produtos_mais_vendidos AS
SELECT
    product_name,
    ROUND(SUM(quantity * unit_price * (1 - COALESCE(discount_pct, 0))),2) AS total_de_vendas

FROM vw_base_vendas
WHERE order_status = 'paid'
GROUP BY product_name
ORDER BY total_de_vendas DESC;
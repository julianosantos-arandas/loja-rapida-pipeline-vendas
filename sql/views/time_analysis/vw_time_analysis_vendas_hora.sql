DROP VIEW IF EXISTS vw_time_analysis_vendas_hora;

CREATE VIEW vw_time_analysis_vendas_hora AS
SELECT
    CAST(strftime('%H', order_time) AS INTEGER) AS order_hour,
    COUNT(*) AS total_pedidos
FROM vw_base_vendas
WHERE order_status IN ('paid', 'returned')
GROUP BY order_hour
ORDER BY total_pedidos DESC;

DROP VIEW IF EXISTS vw_analytics_ticket_medio;

CREATE VIEW vw_analytics_ticket_medio AS
WITH pedidos AS (
    SELECT
        strftime('%Y-%m', order_date) AS ano_mes,
        order_id,
        SUM(quantity * unit_price * (1 - COALESCE(discount_pct, 0))) AS valor_pedido
    FROM vw_base_vendas_financeiras
    WHERE order_status = 'paid'
    GROUP BY ano_mes, order_id
)
SELECT
    ano_mes,
    ROUND(AVG(valor_pedido), 2) AS ticket_medio,
    COUNT(order_id) AS total_pedidos
FROM pedidos
GROUP BY ano_mes
ORDER BY ano_mes;

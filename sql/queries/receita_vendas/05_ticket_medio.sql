SELECT 
    strftime('%Y-%m', order_date) AS ano_mes,
    ROUND(SUM(quantity * unit_price * (1 - COALESCE(discount_pct, 0))) / COUNT(DISTINCT order_id),2)  AS ticket_médio_mensal,
    COUNT(DISTINCT order_id) AS total_pedidos
FROM vendas
WHERE order_status IN ('paid')
GROUP BY ano_mes
ORDER BY ano_mes;   


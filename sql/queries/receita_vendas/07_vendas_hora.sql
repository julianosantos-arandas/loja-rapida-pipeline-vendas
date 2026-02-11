SELECT
    CAST(strftime('%H', order_time) AS INTEGER) AS order_hour,
    COUNT(*) AS total_pedidos
FROM vendas
WHERE order_status IN ('paid', 'returned')
GROUP BY order_hour
ORDER BY total_pedidos DESC;

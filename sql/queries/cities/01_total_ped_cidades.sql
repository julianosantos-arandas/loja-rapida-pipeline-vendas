
SELECT 
    customer_city,
    COUNT(DISTINCT order_id) AS total_pedidos
FROM vendas
GROUP BY customer_city
ORDER BY total_pedidos DESC;


-- Excluir linha NULL na colina customer_city
SELECT 
ROUND (COUNT(*) * 1.0 / COUNT(DISTINCT order_id), 2) AS media_itens_por_pedido
FROM VENDAS;
SELECT
  strftime('%Y-%m', order_date) AS mes,
  COUNT (order_id) AS quantidade_pedidos

FROM vendas
GROUP BY mes
ORDER BY quantidade_pedidos DESC;
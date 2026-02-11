SELECT
    category,
    SUM(unit_price) AS total_vendas

FROM vendas
GROUP BY category
ORDER BY total_vendas DESC;

-- Ajustar a coluna Eletronicos, está faltando acento
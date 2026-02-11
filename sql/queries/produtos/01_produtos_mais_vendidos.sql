SELECT
    product_name,
    Sum(unit_price) AS total_de_vendas

FROM vendas
GROUP BY product_name
ORDER BY total_de_vendas DESC;

-- Retirar a linha produto desconhecidos

SELECT
    order_id,
    order_date,
    order_status,
    quantity,
    unit_price,
    discount_pct,
    quantity * unit_price * (1 - COALESCE(discount_pct, 0)) AS valor_bruto
FROM vendas_inconsistentes
WHERE order_status = 'returned'
  AND quantity * unit_price * (1 - COALESCE(discount_pct, 0)) > 0;
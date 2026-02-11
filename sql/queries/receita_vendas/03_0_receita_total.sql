SELECT
  ROUND(
  SUM (
   quantity * unit_price * (1 - COALESCE(discount_pct, 0))
    ), 
    2
  ) AS receita_total

FROM vendas;

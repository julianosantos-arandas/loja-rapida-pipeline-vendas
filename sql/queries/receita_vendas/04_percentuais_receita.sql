WITH receitas AS ( 
  SELECT ROUND(SUM(quantity * unit_price * (1 - COALESCE(discount_pct, 0))),2) AS receita_total
    FROM vendas
),

receita_paid AS (SELECT ROUND(SUM(quantity * unit_price * (1 - COALESCE(discount_pct, 0))),2) AS valor 
    FROM vendas
    WHERE order_status = 'paid'
),

receita_returned AS (SELECT ROUND(SUM(quantity * unit_price * (1 - COALESCE(discount_pct, 0 ))),2) AS valor 
    FROM vendas
    WHERE order_status = 'returned'
),

receita_cancelled AS (SELECT ROUND(SUM(quantity * unit_price * (1 - COALESCE(discount_pct, 0))),2) AS valor 
    FROM vendas
    WHERE order_status = 'cancelled'
), 

receita_pending AS (SELECT ROUND(SUM(quantity * unit_price * (1 - COALESCE(discount_pct, 0))), 2) AS valor 
    FROM vendas
    WHERE order_status = 'pending'
)

SELECT 
    ROUND((receita_paid.valor / receitas.receita_total) * 100, 2) AS pct_paid,
    ROUND((receita_returned.valor / receitas.receita_total) * 100, 2) AS pct_returned, 
    ROUND((receita_cancelled.valor / receitas.receita_total) * 100, 2) AS pct_cancelled,
    ROUND((receita_pending.valor / receitas.receita_total) * 100, 2) AS pct_pending

FROM receitas, receita_paid, receita_returned, receita_cancelled, receita_pending;
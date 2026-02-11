DROP VIEW IF EXISTS vw_base_vendas_financeiras;

CREATE VIEW vw_base_vendas_financeiras AS
SELECT
    order_id,
    order_date,
    strftime('%Y-%m', order_date) AS ano_mes,
    order_status,
    quantity,
    category,
    unit_price,
    discount_pct,

    -- valor da linha (regra técnica, não KPI)
    ROUND(
    quantity * unit_price * (1 - COALESCE(discount_pct, 0)),
    2
) AS valor_linha_rs

FROM vendas
WHERE order_status IN ('paid', 'returned');

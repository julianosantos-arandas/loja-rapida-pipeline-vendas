DROP VIEW IF EXISTS vw_quality_vendas_excluidas;

CREATE VIEW vw_quality_vendas_excluidas AS
SELECT 
    strftime('%Y-%m', order_date) as ano_mes,

    COUNT(DISTINCT order_id) AS total_pedidos_excluidos,

    SUM(CASE
            WHEN order_status = 'canceled' THEN 1
            ELSE 0
        END
    ) AS total_canceladas,
    
    SUM(CASE
            WHEN order_status = 'pending' THEN 1
            ELSE 0
        END
    ) AS total_pendentes,

    ROUND(
        SUM(
            CASE
                WHEN order_status = 'canceled'
                THEN quantity * unit_price * (1 - COALESCE(discount_pct, 0))
                ELSE 0
            END
        ),
        2
)AS valor_cancelado,
    
    ROUND(
        SUM(
            CASE
                WHEN order_status = 'pending'
                THEN quantity * unit_price * (1 - COALESCE(discount_pct, 0))
                ELSE 0
            END
        ),
        2
)AS valor_pendente,

    ROUND(SUM(quantity * unit_price * (1 - COALESCE(discount_pct,0))),2) AS valor_total_excluido

FROM vendas
WHERE order_status IN ('canceled', 'pending')
GROUP BY ano_mes
ORDER BY ano_mes;
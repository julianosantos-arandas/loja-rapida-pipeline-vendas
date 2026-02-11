DROP VIEW IF EXISTS vw_quality_financeiras_inconsistentes;

CREATE VIEW vw_quality_financeiras_inconsistentes AS
SELECT
    ano_mes,

    COUNT(*) AS total_pedidos_financeiros_inconsistentes,

    SUM(CASE WHEN order_status = 'paid' THEN 1 ELSE 0 END)     AS total_pagos,
    SUM(CASE WHEN order_status = 'returned' THEN 1 ELSE 0 END) AS total_devolucoes,

    -- 🔎 Auditoria (valores brutos, com erro de sinal)
    ROUND(SUM(CASE WHEN order_status = 'paid' THEN valor_bruto ELSE 0 END), 2)
        AS valores_pagos_raw,

    ROUND(SUM(CASE WHEN order_status = 'returned' THEN valor_bruto ELSE 0 END), 2)
        AS valores_devolvidos_raw,

    -- ✅ Negócio (valores corrigidos, sem sinal)
    ROUND(SUM(valor_pago_tratado), 2)      AS valores_pagos_corrigidos,
    ROUND(SUM(valor_devolvido_tratado), 2) AS valores_devolvidos_corrigidos,

    -- 📊 Resultado final (baseado nos valores corrigidos)
    ROUND(
        SUM(valor_pago_tratado) - SUM(valor_devolvido_tratado)
    , 2) AS resultado_total_inconsistentes

FROM (
    SELECT
        strftime('%Y-%m', order_date) AS ano_mes,
        order_status,

        -- valor original (fonte)
        quantity * unit_price * (1 - COALESCE(discount_pct, 0)) AS valor_bruto,

        -- regra de negócio (linha a linha)
        CASE
            WHEN order_status = 'paid'
            THEN ABS(quantity * unit_price * (1 - COALESCE(discount_pct, 0)))
            ELSE 0
        END AS valor_pago_tratado,

        CASE
            WHEN order_status = 'returned'
            THEN ABS(quantity * unit_price * (1 - COALESCE(discount_pct, 0)))
            ELSE 0
        END AS valor_devolvido_tratado

    FROM vendas_inconsistentes
    WHERE order_status IN ('paid', 'returned')
) t
GROUP BY ano_mes
ORDER BY ano_mes;

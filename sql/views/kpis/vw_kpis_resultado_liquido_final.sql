DROP VIEW IF EXISTS vw_kpis_resultado_liquido_final;
CREATE VIEW vw_kpis_resultado_liquido_final AS
SELECT
    ROUND(
        SUM(
            CAST(COALESCE(valores_pagos, 0) AS REAL)
        - CAST(COALESCE(valores_devolvidos, 0) AS REAL)
        ),
        2
    ) AS resultado_liquido
FROM vw_analytics_vendas_financeiras;

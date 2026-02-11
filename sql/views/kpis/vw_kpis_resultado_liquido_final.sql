DROP VIEW IF EXISTS vw_kpis_resultado_liquido_final;

CREATE VIEW vw_kpis_resultado_liquido_final AS
SELECT
    ROUND(
        SUM(
            CASE
                WHEN order_status = 'paid' THEN valor_linha_rs
                WHEN order_status = 'returned' THEN -valor_linha_rs
            END
        ),
        2
    ) AS resultado_liquido
FROM vw_base_vendas_financeiras;

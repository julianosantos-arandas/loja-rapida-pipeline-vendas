DROP VIEW IF EXISTS vw_kpis_resultado_total_v_excluidas;
CREATE VIEW vw_kpis_resultado_total_v_excluidas AS
SELECT
    ROUND(
        SUM(
            CAST(COALESCE(valor_cancelado, 0) AS REAL)
        + CAST(COALESCE(valor_pendente, 0) AS REAL)
        ),
        2
    ) AS total_valor_excluido
FROM vw_quality_vendas_excluidas;
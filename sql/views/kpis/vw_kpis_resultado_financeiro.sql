DROP VIEW IF EXISTS vw_kpis_resultado_financeiro;

CREATE VIEW vw_kpis_resultado_financeiro AS
SELECT
    ROUND(
        SUM(valor_linha_rs),
        2
    ) AS resultado_financeiro
FROM vw_base_vendas_financeiras;

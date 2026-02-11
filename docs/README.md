# Documentação - Loja Rápida

## Problema
Planilhas de vendas espalhadas, sem padrão. A loja não consegue medir faturamento, ticket médio ou devoluções. Precisamos de um ETL simples para organizar tudo.

## Objetivo
Ter um fluxo claro: ler CSVs, validar, limpar, carregar no SQLite e expor camadas (views e CSVs) para análise/BI.

## O que tem aqui
- `01_visão_geral.md` — resumo do projeto e fluxo.
- `02_layout_vendas.md` — colunas esperadas nos CSVs brutos.
- `03_pipeline_vendas.md` — passos do pipeline Python.
- `04_modelo_relacional_vendas.md` — tabelas/views no SQLite.
- `commits.md` — anotações de evolução (se usado).

## Como usar
1) Leia `01_visão_geral.md` para entender o todo.  
2) Confirme se seus CSVs seguem `02_layout_vendas.md`.  
3) Rode o pipeline (`python src/pipelines/pipeline_vendas.py`).  
4) Consulte `04_modelo_relacional_vendas.md` para saber onde os dados ficam no SQLite.  
5) Exporte para BI se precisar (`python src/export/export_views_to_csv.py`).

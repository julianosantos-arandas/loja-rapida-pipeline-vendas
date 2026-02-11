Camada: geral / documentação

# 1. Objetivo do projeto

Ter um pipeline simples de vendas para a loja fictícia “Loja Rápida”: ler CSVs, limpar, gravar em SQLite e gerar views para análise e BI. É exercício de fundamentos, não algo corporativo.

# 2. Tecnologias usadas

- Python (pandas, sqlite3)
- SQLite (banco local)
- Git/GitHub
- Ferramenta de BI (ex.: Power BI) lendo os CSVs exportados

# 3. Fluxo resumido

1. Arquivos `.csv` entram em `data/raw/`.
2. Script `src/pipelines/pipeline_vendas.py` lê, valida (datas, horários, números, textos) e salva em `data/processed/`.
3. Os dados tratados vão para o SQLite em `data/processed/database/loja_rapida.db`.
4. Views SQL em `sql/views` criam camadas: base, quality, analytics, kpis, time_analysis.
5. `src/export/export_views_to_csv.py` exporta cada view para CSVs em `data/bi/`.

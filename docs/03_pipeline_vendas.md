Camada: pipeline de vendas

# Pipeline de Vendas – Loja Rápida

Documento rápido sobre o que o pipeline faz e como ele ajuda a tirar a loja do caos das planilhas.

## 1. Problema que o pipeline resolve
- CSVs chegam bagunçados (tipos errados, valores inválidos, status fora do padrão).
- Sem limpeza, a loja não consegue calcular métricas básicas (faturamento, ticket médio, devoluções).
- Precisamos de um ETL simples e repetível para entregar dados confiáveis.

## 2. Objetivo
- Ler todos os CSVs em `data/raw/`.
- Validar e limpar campos-chave (datas, horas, números, textos).
- Carregar os dados limpos no SQLite (`data/processed/database/loja_rapida.db`).
- Manter camadas claras: base, quality, analytics, kpis e exportar para BI.

## 3. Entradas e saídas

### Entrada (RAW)
- Pasta: `data/raw/`
- Arquivos `.csv` com possíveis inconsistências (tipos, valores, regras de negócio).

### Saídas principais
- `data/processed/base/vendas_prepared.csv` — base limpa.
- `data/processed/quality/vendas_excluidas.csv` — pending/canceled.
- `data/processed/analytics/vendas_financeiras.csv` — paid/returned.
- `data/processed/quality/vendas_inconsistentes.csv` — registros financeiros com problema de dados.
- Banco SQLite populado em `data/processed/database/loja_rapida.db`.

## 4. Regras aplicadas (resumo)
- Datas e horas: precisam ser válidas.
- Números: `quantity > 0`, `unit_price > 0`, `0 <= discount_pct <= 1`.
- Status: normaliza e filtra valores esperados (`paid`, `returned`, `pending`, `canceled`).
- Linhas que falham viram parte dos datasets de qualidade (excluídos ou inconsistentes).

## 5. Fluxo do código (alto nível)
Arquivo: `src/pipelines/pipeline_vendas.py`

1) `load_all_sales_file()` — lê e concatena todos os CSVs de `data/raw/`.  
2) `clean_raw_sales()` — valida datas/horas, converte números, aplica regras de negócio.  
3) `run_excluded()` — separa `pending` e `canceled` em `quality/vendas_excluidas.csv`.  
4) `run_financial()` — separa `paid` e `returned` em `analytics/vendas_financeiras.csv`.  
5) `run_inconsistent()` — identifica registros financeiros com números inválidos e salva em `vendas_inconsistentes`.  
6) `ensure_db_schema()` — recria tabelas e views a partir de `sql/ddl` e `sql/views`.  
7) Carga no SQLite — popula `vendas` e `vendas_inconsistentes`.  
8) Exportar para BI (passo separado em `src/export/export_views_to_csv.py`).

## 6. Logs esperados
- Quantidade de linhas lidas em RAW.
- Quantidade de linhas após limpeza.
- Quantidade de linhas excluídas (pending/canceled).
- Quantidade de linhas financeiras (paid/returned).
- Quantidade de inconsistentes.
- Caminhos dos arquivos gerados.

## 7. Quando rodar de novo
- Chegou CSV novo em `data/raw/`.
- Ajustou alguma view SQL.
- Mudou regra de limpeza ou domínio de status.

## 8. Próximos passos possíveis
- Adicionar mais validações (ex.: listas de payment_method/channel permitidas).
- Criar testes automáticos cobrindo as funções de limpeza.
- Alertas simples quando o volume de inconsistentes passar de um limite.

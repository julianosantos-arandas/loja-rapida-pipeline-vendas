# Loja Rápida - Pipeline de Vendas



## Problema
A loja fictícia tem várias planilhas soltas de vendas. Sem padrão, ela não consegue acompanhar faturamento, ticket médio ou devoluções. Falta um processo ETL para tirar os dados do caos e entregar algo confiável para análise.

## Objetivo
Construir um ETL básico que leia CSVs, valide, limpe, carregue no SQLite e gere views/CSVs prontos para BI. Ideia é ter um fluxo repetível e auditável, fácil de entender.

## O que é
- Pipeline pequeno para organizar dados de vendas de uma loja fictícia.
- Usa Python (pandas + sqlite3) para montar base limpa e views em SQL.
- Exporta CSVs prontos para BI em `data/bi`.

## Como preparar o ambiente
- Python 3.11+ resolve. Se existir `requirements.txt`, rode `pip install -r requirements.txt`.
- Tudo roda local, o banco é SQLite em `data/processed/database/loja_rapida.db`.

## Passo a passo para rodar
- Coloque os CSVs brutos em `data/raw` (qualquer nome, mas precisa terminar com `.csv`).
- Execute o pipeline: `python src/pipelines/pipeline_vendas.py`
  - Limpa os dados, separa em camadas e carrega no SQLite.
- Exporte as views para BI: `python src/export/export_views_to_csv.py`
  - Cria CSVs em `data/bi` organizados por pastas (analytics, quality, kpis, base, time_analysis).

## O que o pipeline faz
- Lê todos os CSVs de `data/raw` e concatena.
- Valida datas, horários e números (quantidade, preço, desconto) e remove linhas inválidas.
- Salva a base preparada em `data/processed/base/vendas_prepared.csv`.
- Gera subconjuntos: financeiros (paid/returned) e excluídos (pending/canceled).
- Identifica registros financeiros com problemas e guarda em `vendas_inconsistentes`.
- Recria as tabelas/views definidas em `sql/ddl` e `sql/views` no banco SQLite.

## Estrutura principal
- `src/pipelines/pipeline_vendas.py` → limpeza, splits e carga no SQLite.
- `src/export/export_views_to_csv.py` → exporta cada view para CSVs de BI.
- `sql/ddl` → criação de tabelas base (`vendas`, `vendas_inconsistentes`).
- `sql/views` → views de base, analytics, qualidade, KPIs e análise por hora.
- `data/raw` → entrada bruta (coloque seus CSVs aqui).
- `data/processed` → saídas do pipeline (não versionar).
- `data/bi` → CSVs finais para dashboards.

## Testes rápidos
- Se tiver testes, rode `pytest` na raiz.
- Sem testes? Abra o SQLite (`sqlite3 data/processed/database/loja_rapida.db`) e confira se a tabela `vendas` tem linhas.

## Dicas finais
- Sempre rode o pipeline antes de exportar para BI.
- Alterou alguma view SQL? Rode o pipeline de novo para recriar tudo no banco.

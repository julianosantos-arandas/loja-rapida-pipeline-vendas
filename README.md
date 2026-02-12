![Python](https://img.shields.io/badge/language-Python-blue)

Loja Rápida — Pipeline de Vendas

🔵 Sobre o projeto

Este é meu primeiro projeto completo de engenharia de dados.

O projeto simula o cenário de uma loja fictícia chamada Loja Rápida, que utilizava apenas planilhas soltas para registrar vendas, sem um processo estruturado para controle de métricas e qualidade dos dados.

A proposta foi organizar esse fluxo por meio de um pipeline simples em Python com SQLite, estruturando os dados em camadas e criando uma base confiável para análise.

🔵 Problema

A ausência de um processo estruturado gerava:

🔹 Dificuldade para acompanhar o faturamento mensal

🔹 Falta de controle sobre registros inconsistentes

🔹 Ausência de indicadores consolidados (ticket médio, produtos mais vendidos, faturamento por cidade)

🔹 Risco elevado de erro manual

🔵 Solução

Foi desenvolvido um pipeline com as seguintes etapas:

1️⃣ Ingestão de dados brutos

2️⃣ Tratamento e padronização

3️⃣ Separação de registros inconsistentes

4️⃣ Modelagem por meio de views analíticas

5️⃣ Exportação de dados para consumo em BI

🔵 Tecnologias utilizadas

🔹 SQLite

🔹 Git

🔹 Power BI

🔹 Python

🔹 Pandas

🔵 Dashboard

O dashboard foi construído a partir das views analíticas geradas no pipeline.

🔹 Visão Geral
![Visão Geral](docs/Loja_Rapida_BI/images/visao_geral.png)

🔹 Monitoramento de Inconsistências
![Governança](docs/Loja_Rapida_BI/images/governanca_inconsistentes.png)


Para documentação detalhada do dashboard:
docs/dashboard.md


🔵 Aprendizados

Durante o desenvolvimento, aprofundei conhecimentos em:

🔹 Organização de projetos de dados

🔹 Estruturação em camadas (base, quality, analytics)

🔹 Manipulação de dados com Pandas

🔹 Criação de views analíticas em SQL

🔹 Versionamento com Git

🔵 Como baixar o projeto

Opção 1 — Via Git (recomendado)

Clone o repositório:

git clone https://github.com/julianosantos-arandas/loja-rapida-pipeline-vendas.git
cd loja-rapida-pipeline-vendas

🔵 Como executar o projeto

1️⃣ Criar ambiente virtual Linux / macOS:
   python3 -m venv .venv
   source .venv/bin/activate

   Criar ambiente virtual Windows (PowerShell):
   python -m venv .venv
   .venv\Scripts\Activate


2️⃣ Instalar dependências:
   pip install -r requirements.txt

3️⃣ Executar o pipeline
   python src/pipelines/pipeline_vendas.py

Após a execução, o banco SQLite será criado automaticamente em:
data/processed/database/loja_rapida.db


🔵 Como consultar o banco e as views

Após rodar o pipeline, o banco SQLite é criado em:

🔹 data/processed/database/loja_rapida.db

Para visualizar as tabelas e views:

🔹 sqlite3 data/processed/database/loja_rapida.db

Dentro do SQLite:
   .tables
   .schema nome_da_view 
    Exemplo: .schema vw_analytics_faturamento_mensal ➡️ Isso exibirá o SQL utilizado na criação da view.


🔵 Próximos passos

Este projeto representa minha base em organização e estruturação de dados.
Nos próximos projetos pretendo evoluir para automação, testes e ferramentas mais robustas do ecossistema de dados.

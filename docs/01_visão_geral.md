Camada: geral / documentação

# 1. Objetivo do projeto

Criar um mini pipeline de dados de vendas para a empresa fictícia “Loja Rápida”, 
organizando arquivos brutos de vendas, limpando os dados e carregando tudo em um 
banco SQL para análise.

# 2. Tecnologias usadas (por enquanto)

- Git (controle de versão)
- Python (scripts de ingestão e tratamento de dados)
- SQL + banco relacional (armazenar e consultar as vendas)
- Pasta de dados local (`data/raw` e `data/processed`)
- Linha de comando (Linux/terminal)

# 3. Visão geral do fluxo (alto nível)

- Arquivos de vendas chegam na pasta `data/raw/`
- Um script em Python lê esses arquivos, faz validações e limpeza
- O resultado é salvo em `data/processed/`
- Esses dados são carregados em um banco SQL
- Consultas em `sql/queries/` respondem perguntas do negócio 
  (vendas por dia, top produtos, clientes mais valiosos etc.)

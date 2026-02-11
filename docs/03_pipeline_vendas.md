Camada: pipeline de vendas

# Pipeline de Vendas – Loja Rápida

Este documento descreve o comportamento do pipeline de vendas implementado em `src/pipelines/pipeline_vendas.py`.

---

## 1. Objetivo do pipeline

- Ingerir arquivos **brutos** de vendas da Loja Rápida que chegam na pasta `data/raw/`.
- Aplicar regras de **qualidade de dados** e **regras de negócio**.
- Gerar um arquivo consolidado e limpo em `data/processed/` para uso posterior em SQL / análises.

---

## 2. Entradas e saídas

### 2.1 Entrada (RAW)

- Pasta: `data/raw/`
- Arquivos de exemplo:
  - `vendas_2024-07_messy.csv`
  - `vendas_2024-08_messy.csv`
  - `vendas_2024-09_messy.csv`
  - `vendas_2024-10_messy.csv`
  - `vendas_2024-11_messy.csv`
- Conteúdo: arquivos CSV “bagunçados” com possíveis:
  - tipos errados,
  - valores inválidos,
  - quebras de regra de negócio.

### 2.2 Gabarito de referência (clean)

- Pasta: `data/processed/`
- Arquivo: `vendas_2024-11_clean.csv`
- Papel: servir de **referência** (gabarito) para comparar com o resultado do pipeline.

### 2.3 Saída (prepared)

- Pasta: `data/processed/`
- Arquivo gerado pelo pipeline: `vendas_prepared.csv`
- Conteúdo: somente linhas que:
  - passaram nas conversões numéricas,
  - NÃO violam as regras de negócio definidas.

---

## 3. Layout e regras aplicadas

### 3.1 Colunas principais

Ver detalhes em `docs/02_layout_vendas.md`.  
Principais colunas usadas nas regras:

- `quantity`
- `unit_price`
- `discount_pct`
- `order_id`
- `order_date`
- `order_time`
- `customer_id`
- `product_id`
- `channel`
- `order_status`

### 3.2 Regras de qualidade de dados (tipagem)

Aplicadas dentro da função `clean_raw_sales(df_raw)`:

1. **Conversão para numérico**

   Colunas consideradas numéricas:
   - `quantity`
   - `unit_price`
   - `discount_pct`

   Regra:
   - Tentar converter essas colunas para número (`pd.to_numeric`).
   - Valores inválidos (ex.: `"FREE"`, `"three"`, `"349,90"`, vazio)  
     ➜ viram `NaN`.

2. **Remoção de linhas com problema numérico**

   - Qualquer linha com `NaN` em `quantity`, `unit_price` ou `discount_pct`
     é considerada **inválida** nesta etapa.
   - Essas linhas são removidas.
   - O pipeline registra:
     - quantas linhas tinham problemas numéricos,
     - quantas linhas restaram após essa filtragem.

### 3.3 Regras de negócio

Depois do filtro numérico, são aplicadas regras de negócio:

- `quantity > 0`
- `unit_price > 0`
- `0 <= discount_pct <= 1`

Linhas que **violam** qualquer uma dessas condições são removidas.  
O pipeline registra:

- quantas linhas violaram as regras de negócio,
- quantas linhas restaram após aplicar essas regras.

---

## 4. Fluxo da pipeline (alto nível)

Função principal: `run_raw_pipeline()`.

1. **Carregar dados brutos**
   - Chama `load_all_sales_file()`.
   - Lê todos os arquivos `.csv` em `data/raw/` e concatena em um único DataFrame `df_raw`.
   - Imprime: `Total de linhas carregadas de raw`.

2. **Carregar gabarito clean**
   - Chama `load_reference_clean_sales()`.
   - Lê `data/processed/vendas_2024-11_clean.csv` em `df_clean_ref`.
   - Imprime: `Total de linhas no gabarito clean`.

3. **Limpar e aplicar regras**
   - Chama `clean_raw_sales(df_raw)`, que:
     - cria uma cópia de trabalho (`df`),
     - converte `quantity`, `unit_price`, `discount_pct` para numérico,
     - remove linhas com valores numéricos inválidos,
     - aplica regras de negócio,
     - devolve `df_business_valid` como `df_prepared`.
   - Imprime:
     - linhas com problema numérico,
     - linhas restantes após remover inválidas,
     - linhas que violam regras de negócio,
     - linhas restantes após aplicar regras de negócio.

4. **Salvar saída preparada**
   - Monta o caminho: `data/processed/vendas_prepared.csv`.
   - Salva o `df_prepared` com `to_csv(..., index=False)`.
   - Imprime: `Arquivo preparado salvo em: ...`.

5. **Comparação de contagem com o gabarito**
   - Calcula:
     - `len(df_prepared)` → total de linhas preparadas,
     - diferença em relação a `len(df_clean_ref)`.
   - Imprime:
     - `Total de linhas no dataset preparado`,
     - `Diferença de linhas entre gabarito clean e preparado`.

---

## 5. Exemplo de execução (log resumido)

Exemplo real de uma execução do pipeline:

- Total de linhas carregadas de raw: **8**
- Total de linhas no gabarito clean: **12**
- Linhas com valores numéricos inválidos (`quantity/unit_price/discount_pct`): **1**
- Linhas restantes após remover inválidas: **7**
- Linhas que violam regras de negócio (`quantity>0, unit_price>0, 0<=discount_pct<=1`): **2**
- Linhas restantes após aplicar regras de negócio: **5**
- Arquivo preparado salvo em: `data/processed/vendas_prepared.csv`
- Total de linhas no dataset preparado: **5**
- Diferença de linhas entre gabarito clean e preparado: **7**

*(Esses valores podem mudar se os arquivos RAW forem alterados.)*

---

## 6. Próximos passos planejados

- Carregar `vendas_prepared.csv` em um **banco relacional** (ex.: SQLite).
- Criar scripts SQL em `sql/ddl/` para:
  - criar a tabela de vendas.
- Escrever queries em `sql/queries/` para:
  - vendas por dia,
  - vendas por canal,
  - top produtos, etc.
- Adicionar mais validações (datas inválidas, status desconhecidos, etc.).

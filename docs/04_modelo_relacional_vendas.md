# Modelo relacional - Tabela `vendas`
Versão: 1.0  
Autor: Juliano  
Contexto: Projeto Loja_Rápida_p_v - pipeline de vendas

> Visão simples do modelo relacional que resolve o problema de planilhas soltas.

## 1. Problema e objetivo
- Planilhas sem padrão não garantem integridade (linhas duplicadas, status errados).
- Precisamos de uma tabela estável para análises: cada linha é um item de pedido limpo.

Camada: **relacional / consumo analítico** (dados já limpos vindos do pipeline).

## 2. Nome da tabela

- Nome lógico: `vendas`
- Sugestão de nome físico: `dw_vendas`ou `fato_vendas` (para projetos maiores. por enquanto manter apenas `vendas`)

## 3. Chave primária e granularidade
### 3.1 Granularidade
- **Uma linha = um item de pedido**. Se o pedido 1001 tiver 3 produtos, são 3 linhas.

### 3.2 Chave primária (v1)
- `order_id` + `product_id`.
- Motivo: pedido pode ter vários produtos. No futuro dá para criar um `order_item_id`.

## 4. Definição das colunas


| Coluna         | Tipo SQL          | NOT NULL? | Descrição                                                                                 |
|----------------|-------------------|-----------|-------------------------------------------------------------------------------------------|
| order_id       | INTEGER           | SIM       | Identificador do pedido. Vem do sistema transacional.                                    |
| order_date     | DATE              | SIM       | Data do pedido (`YYYY-MM-DD`).                                                           |
| order_time     | TIME              | NÃO       | Horário do pedido (`HH:MM`).                                                             |
| customer_id    | INTEGER           | SIM       | Identificador único do cliente.                                                          |
| customer_city  | VARCHAR(100)      | NÃO       | Cidade do cliente.                                                                       |
| product_id     | INTEGER           | SIM       | Identificador único do produto.                                                          |
| product_name   | VARCHAR(200)      | SIM       | Nome do produto no momento da venda.                                                     |
| category       | VARCHAR(100)      | NÃO       | Categoria do produto (Calçados, Eletrônicos, Moda, etc.).                                |
| quantity       | INTEGER           | SIM       | Quantidade de itens na linha do pedido.                                                  |
| unit_price     | NUMERIC(10,2)     | SIM       | Preço unitário do produto na moeda padrão.                                               |
| discount_pct   | NUMERIC(5,2)      | NÃO       | Percentual de desconto entre 0 e 1 (10% = 0.10).                                         |
| payment_method | VARCHAR(50)       | NÃO       | Método de pagamento (ex.: `credit_card`, `boleto`, `pix`).                               |
| channel        | VARCHAR(50)       | NÃO       | Canal de venda (ex.: `website`, `mobile_app`, `marketplace`).                            |
| order_status   | VARCHAR(20)       | SIM       | Status do pedido (ex.: `paid`, `canceled`, `returned`).                                  |

> Observação: `NOT NULL = SIM` significa que a coluna será criada como `... NOT NULL` no banco, ou seja, é **obrigatória**.

## 5. Regras de negócio e restrições recomendadas

Estas regras devem ser consideradas no momento de criar a tabela em SQL (via `CHECK`, tipos corretos, etc.) e também na etapa de limpeza no Python.

### 5.1 Regras de consistência numérica
- `quantity > 0`.
- `unit_price > 0`.
- `discount_pct` entre `0` e `1` (0% a 100%).

### 5.2 Regras de data e hora
- `order_date` deve ser data válida.
- `order_time` (quando presente) entre `00:00` e `23:59`.

### 5.3 Regras de chave e duplicidade
- `(order_id, product_id)` não pode repetir.

### 5.4 Domínios de status e listas controladas
- `order_status` dentro de `paid`, `returned`, `pending`, `canceled`.
- `payment_method` e `channel` podem ganhar listas controladas depois.

## 6. Relações futuras (ideia, não implementado)
- `clientes` (dim): `customer_id` como FK.
- `produtos` (dim): `product_id` como FK.
- `calendario` (dim): ligada por `order_date`.


## 7. Observações de implementação
- Use esta definição ao criar a tabela (`sql/ddl/01_create_table_vendas.sql`) e ao validar dados no Python.
- Se mudar coluna/tipo/chave, registre uma nova versão (v1.1, v1.2, …) e documente.

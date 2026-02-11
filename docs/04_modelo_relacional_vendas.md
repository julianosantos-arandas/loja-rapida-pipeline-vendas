# Modelo relacional - Tabela `vendas`
Versão: 1.0 
Autor: Juliano 
Contexto: Projeto Loja_Rápida_p_v -  Desafio de pipeline de vendas


## 1. Objetivo da tabela

A tabela`vendas` armazena **uma linha por item de pedido**.
Cada linha representa um produto vendido em um pedido, incluindo informações do cliente, produto, canal, pagamento e status do pedido.

Camada: **relacional / consumo analítico** (dados já limpos vindos do pipeline).


## 2. Nome da tabela

- Nome lógico: `vendas`
- Sugestão de nome físico: `dw_vendas`ou `fato_vendas` (para projetos maiores. por enquanto manter apenas `vendas`)

## 3. Chave primária e granularidade
(Chave primária = coluna(s) que identificam cada linha de forma única.)
(Granularidade = “o que uma linha representa?” (pedido? item? dia? cliente?).)
### 3.1 Granularidade (o que é uma linha?)

- **Uma linha = um item de pedido**
  Exemplo: se o pedido `1001` tiver 3 produtos diferentes, teremos 3 linhas na tabela `vendas`.

### 3.2 Chave primária (versão inicial)

- **Chave primária sugerida (v1): **
   - `order_id` + `product_id`
  
Motivo: um mesmo pedido pode ter vários produtos.
Mais para frente poderíamos criar uma coluna `order_item_id` exclusiva, mas por enquanto a combinação `order_id + product_id_ é suficiente.

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
| discount_pct   | NUMERIC(5,2)      | NÃO       | Percentual de desconto entre 0 e 1 (10% = 0.10).                                        |
| payment_method | VARCHAR(50)       | NÃO       | Método de pagamento (ex.: `credit_card`, `boleto`, `pix`).                               |
| channel        | VARCHAR(50)       | NÃO       | Canal de venda (ex.: `website`, `mobile_app`, `marketplace`).                            |
| order_status   | VARCHAR(20)       | SIM       | Status do pedido (ex.: `paid`, `canceled`, `returned`).                                  |

> Observação: `NOT NULL = SIM` significa que a coluna será criada como `... NOT NULL` no banco, ou seja, é **obrigatória**.

## 5. Regras de negócio e restrições recomendadas

Estas regras devem ser consideradas no momento de criar a tabela em SQL (via `CHECK`, tipos corretos, etc.) e também na etapa de limpeza no Python.

### 5.1 Regras de consistência numérica

- `quantity > 0 `
   - Linhas com `quantity <= 0` devem ser tratadas (corrigidas ou descartadas)
 - `unit_price >=0`
   - Valores negativos não são permitidos.
 - `discount_pct`:
   - Deve estar entre `0` e `1` (0% a 100%).
   - Valores fora desse intervalo devem ser tratados como erro.
  
### 5.2 Regras de data e hora

- `order_date` deve ser uma data válida (sem valores absurdos, ex.: ano 1900 ou 2099, dependendo da regra de negócio).
- `order_time` (quando presente) deve ser um horário válido (`00:00` a `23:59`)

### 5.3. Regras de chave e duplicidade

- A combinação `(order_id, product_id)` **não deve se repetir**.
- Se forem detectadas duplicidades, devem ser investigadas e tratadas pelo pipeline.

### 5.4. Regras de status e domínio de valores

- `order_status` deve estar dentro de um conjunto controlado, por exemplo:
  - `paid`, `canceled`, `returned`, `pending`
- `payment_method` e `channel` também podem ser validados contra listas de valores permitidos no futuro (domínios controlados).

## 6. Relações futuras (visão de crescimento do modelo)

> **Não precisa implementar agora**, mas já fica registrado para versão futura do modelo:

- Tabela `clientes`:
  - `customer_id` como chave primária.
  - `vendas.customer_id` seria uma **chave estrangeira** para `clientes.customer_id`.

- Tabela `produtos`:
  - `product_id` como chave primária.
  - `vendas.product_id` seria chave estrangeira para `produtos.product_id`.

- Tabela `calendario`:
  - Tabela de datas (`dim_calendario`) ligada por `order_date`.


## 7. Observações de implementação

- Esta documentação serve como base para:
  - criação da tabela em SQL (`CREATE TABLE vendas (...)`);
  - validações na etapa de limpeza em Python;
  - entendimento do modelo por outros devs / analistas.

- Qualquer alteração estrutural (novas colunas, mudança de tipo, mudança de chave) deve ser registrada como **nova versão** deste arquivo (ex.: v1.1, v1.2).

Camada: raw

# Layout dos arquivos de vendas

## Colunas e significados

**order_id**
  
Identificador dos pedidos
Exemplos de valores: (1101, 1002, 1003,...).

**order_date**

Data do pedido no formato: `YYYY-MM-DD`.

**order_time**

Horário do pedido no formato: `HH:MM`.

**customer_id**

Identificador único do cliente.

**customer_city**

Cidade do cliente.

**product_id**

Identificador do único do produto.

**product_name**

Nome do produto vendido.

**category**

Categoria do produto vendido (por exemplo: Calçados, Eletrônicos, Moda, etc).

**quantity**

Quantidade do produto vendido.

**unit_price**

Preço unitário do produto.

**discount_pct**

Percentual de desconto aplicado na venda (0 a 1 onde 10% = 0.10).

**payment_method**

Metodo de pagamento (por exemplo: credit card, boleto, etc).

**channel**

Canal onde foi efetuado a compra (por exemplo: mobile_app, marketplace, etc).

**order_status**

Status do pedido (por exemplo: paid, etc)

**Regras esperadas**

- `order_date` deve ser uma data válida.
- `order_time` deve ser um horário válido.
- `customer_id` não deve ser vazio.
- `quantity`> 0
- `discount_pct` deve ser 0 a 10 - 0.1 = 10%.


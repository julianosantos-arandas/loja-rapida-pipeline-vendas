Camada: raw

# Layout dos arquivos de vendas

## Colunas e significado rápido

- **order_id** — identificador do pedido (ex.: 1101).
- **order_date** — data `YYYY-MM-DD`.
- **order_time** — hora `HH:MM`.
- **customer_id** — id do cliente (não pode faltar).
- **customer_city** — cidade do cliente.
- **product_id** — id do produto.
- **product_name** — nome do produto.
- **category** — categoria (Ex.: Calçados, Eletrônicos).
- **quantity** — quantidade vendida.
- **unit_price** — preço unitário.
- **discount_pct** — desconto de 0 a 1 (ex.: 0.10 = 10%).
- **payment_method** — forma de pagamento (ex.: credit_card, boleto).
- **channel** — canal da compra (ex.: mobile_app, marketplace).
- **order_status** — status (paid, returned, pending, canceled).

## Regras básicas que o pipeline espera
- `order_date` e `order_time` precisam ser válidos.
- `quantity` > 0.
- `unit_price` > 0.
- `discount_pct` entre 0 e 1.
- `order_status` dentro dos valores esperados (paid, returned, pending, canceled).
- `customer_id` não pode ser vazio.



🔵  Objetivo

O dashboard foi desenvolvido para visualizar os dados processados pelo pipeline
e acompanhar indicadores financeiros da Loja Rápida.

As visualizações foram construídas a partir das views analíticas geradas no banco SQLite.


🔵  Fonte dos dados

O dashboard consome dados do banco:

data/processed/database/loja_rapida.db

As métricas são derivadas das seguintes views:

🔹 vw_analytics_faturamento_mensal
🔹 vw_analytics_ticket_medio
🔹 vw_analytics_faturamento_por_cidades
🔹 vw_kpis_resultado_liquido_final
🔹 vw_analytics_vendas_inconsistentes


🔵 Principais Indicadores

1️⃣ Faturamento Mensal

Calculado a partir da soma do valor total das vendas com status financeiro válido.

Origem: vw_analytics_faturamento_mensal


2️⃣ Ticket Médio

Calculado como:

valor_total / quantidade_de_pedidos

Origem: vw_analytics_ticket_medio


3️⃣ Resultado Líquido

Diferença entre valores pagos e valores devolvidos.

Origem: vw_kpis_resultado_liquido_final


4️⃣ Monitoramento de Inconsistências

Exibe vendas com impacto financeiro que foram removidas da camada analítica
por apresentarem inconsistências técnicas (ex: quantidade negativa,
preço inválido, desconto incorreto).

Origem: vw_analytics_vendas_inconsistentes

🔵 Decisões dos KPIs

O ticket médio considera apenas vendas com status paid, pois são as que realmente geram receita.

As devoluções (returned) foram analisadas separadamente, pois representam valores que saíram do caixa após a venda.

Registros com erro técnico (quantidade negativa, preço inválido, desconto incorreto) foram removidos da camada analítica para não distorcer os indicadores, mas continuam armazenados para controle.

A ideia foi trabalhar com dados mais confiáveis sem perder rastreabilidade.

🔵 Observações

O objetivo do dashboard não é apenas apresentar métricas,
mas também demonstrar a separação entre:

🔹 Camada Base
🔹 Camada de Qualidade
🔹 Camada Analítica
🔹 Camada de KPIs

O painel reflete essa estrutura de organização.

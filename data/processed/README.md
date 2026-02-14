# Dados processados (gerados)


Regras rápidas:
- Não versionar esta pasta (só arquivos de trabalho temporário).
- O banco SQLite fica em `data/processed/database/loja_rapida.db`.
- Outras saídas ficam em `data/processed/base`, `quality`, `analytics`.

Como gerar:
1. Rodar `python src/pipelines/pipeline_vendas.py`.
2. Conferir se os arquivos apareceram nas subpastas acima.

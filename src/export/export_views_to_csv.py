# bloco 1
import os
import sqlite3
import pandas as pd
from pathlib import Path
from dotenv import load_dotenv

# carregar variáveis de ambiente
load_dotenv()
# bloco 2
PROJECT_ROOT = os.getenv("PROJECT_ROOT")
if not PROJECT_ROOT:
    raise EnvironmentError(
        "Variável de ambiente PROJECT_ROOT não definida. "
        "Crie um arquivo .env ou defina a variável no sistema."
    )

# bloco 3
BASE_DIR = Path(PROJECT_ROOT)
DB_PATH = BASE_DIR / "data" / "processed" / "loja_rapida.db"
BI_DIR = BASE_DIR / "data" / "bi"

EXPORT_MAP = {
    "vw_analytics_faturamento_mensal": ("analytics", "faturamento_mensal.csv"),
    "vw_analytics_ticket_medio": ("analytics", "ticket_medio.csv"),
    "vw_analytics_faturamento_por_cidades": ("analytics", "faturamento_por_cidades.csv"),
    "vw_analytics_produtos_mais_vendidos": ("analytics", "produtos_mais_vendidos.csv"),
    "vw_analytics_vendas_financeiras": ("analytics", "vendas_financeiras.csv"),
    "vw_analytics_categoria_mais_vendida": ("analytics", "categoria_mais_vendida.csv"),
    "vw_analytics_categorias_retornadas": ("analytics", "categorias_retornadas.csv"),

    "vw_quality_vendas_excluidas": ("quality", "vendas_excluidas.csv"),
    "vw_quality_financeiras_inconsistentes": ("quality", "financeiras_inconsistentes.csv"),

    "vw_kpis_resultado_financeiro": ("kpis", "kpi_resultado_financeiro.csv"),
    "vw_kpis_resultado_liquido_final": ("kpis", "kpi_resultado_liquido.csv"),
    "vw_kpis_resultado_total_v_excluidas": ("kpis", "kpi_vendas_excluidas.csv"),

    "vw_base_vendas_financeiras": ("base", "base_vendas_financeiras.csv"),
    "vw_base_vendas": ("base", "base_vendas.csv"),
    "vw_time_analysis_vendas_hora": ("time_analysis", "vendas_hora"),
}

# bloco 4
def export_views_to_bi():
    conn = sqlite3.connect(DB_PATH)

    try:
        for view_name, (layer, filename) in EXPORT_MAP.items():
            output_dir = BI_DIR / layer
            output_dir.mkdir(parents=True, exist_ok=True)

            output_path = output_dir / filename

            df = pd.read_sql_query(
                f"SELECT * FROM {view_name}",
                conn
            )

            df.to_csv(output_path, index=False)
            print(f"✔ Exportado: {view_name} → {output_path}")

    finally:
        conn.close()

if __name__ == "__main__":
    export_views_to_bi()

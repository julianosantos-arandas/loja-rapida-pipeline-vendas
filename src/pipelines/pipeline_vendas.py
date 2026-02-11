import os
import pandas as pd
import sqlite3
from pathlib import Path

RAW_DATA_DIR = os.path.join("data", "raw")
PROCESSED_DATA_DIR = os.path.join("data", "processed")

BASE_DIR = os.path.join(PROCESSED_DATA_DIR, "base")
QUALITY_DIR = os.path.join(PROCESSED_DATA_DIR, "quality")
ANALYTICS_DIR = os.path.join(PROCESSED_DATA_DIR, "analytics")
DATABASE_DIR = os.path.join(PROCESSED_DATA_DIR, "database")

DB_PATH = os.path.join(DATABASE_DIR, "loja_rapida.db")

for directory in [
    BASE_DIR,
    QUALITY_DIR,
    ANALYTICS_DIR,
    DATABASE_DIR,
]:
    os.makedirs(directory, exist_ok=True)


def load_all_sales_file():
    """Carregar todos os arquivos CSV de vendas brutos (messy) da pasta RAW_DATA_DIR e retornar um único DataFrame."""

    dfs = []

    for file_name in os.listdir(RAW_DATA_DIR):
        # O for itera sobre a lista, e a variável file_name recebe cada item em cada iteração
        # verifica se o nome do arquivo termina com ".csv".
        if file_name.endswith(".csv"):

            file_path = os.path.join(RAW_DATA_DIR, file_name)
            # pd.read_csv(file_path) usa o pandas para ler o arquivo .csv cujo caminho completo está em file_path.
            # O resultado é um DataFrame (tabela em memória) com todas as colunas e linhas daquele arquivo.
            df = pd.read_csv(file_path)
            # dfs.append(df) pega o DataFrame lido do arquivo atual (df) e adiciona dentro dessa lista.
            dfs.append(df)
            # pd.concat(dfs, ignore_index=True) junta (concatena) todos os DataFrames da lista dfs em um único DataFrame.
    return pd.concat(dfs, ignore_index=True)


def load_reference_clean_sales():
    """Carregar o arquivo de vendas limpo (gabarito) da pasta PROCESSED_DATA_DIR."""

    clean_path = os.path.join(BASE_DIR, "vendas_2024-11_clean.csv")

    return pd.read_csv(clean_path)


def run_raw_pipeline():
    """Executar o pipeline de dados brutos e preparar a base para comparação com o gabarito clean."""
    print("LENDO CSV")
    df_raw = load_all_sales_file()

    print(f"Total de linhas carregadas de raw: {len(df_raw)}")

    df_clean_ref = load_reference_clean_sales()

    print(f"Total de linhas no gabarito clean: {len(df_clean_ref)}")

    df_prepared = clean_raw_sales(df_raw)
    
    run_excluded(df_prepared)

    run_financial(df_prepared)
    
    output_path = os.path.join(BASE_DIR, "vendas_prepared.csv")
    
    df_prepared.to_csv(output_path, index=False)
    
    print(f"Arquivo preparado salvo em: {output_path}")

    print(f"Total de linhas no dataset preparado: {len(df_prepared)}")

    df_inconsistent = run_inconsistent(df_raw)

    output_path_inc = os.path.join(QUALITY_DIR, "vendas_inconsistentes.csv")

    df_inconsistent.to_csv(output_path_inc, index=False)

    print(f"Arquivo inconsistente salvo em: {output_path_inc}")

    print(f"Total de linhas no dataset inconsistentes: {len(df_inconsistent)}")

    conn = sqlite3.connect(DB_PATH)

    # Garante schema
    ensure_db_schema(conn)

    conn.execute("DELETE FROM vendas")
    conn.commit()

    # Carrega dados no banco (gold)
    df_prepared.to_sql(
        "vendas",
        conn,
        if_exists="append",
        index=False
    )

    conn.execute("DELETE FROM vendas_inconsistentes")
    conn.commit()

    df_inconsistent.to_sql(
        "vendas_inconsistentes",
        conn,
        if_exists="append",
        index=False
    )

    conn.close()

    diff_vs_clean = len(df_prepared) - len(df_clean_ref)

    print(
        f"Diferença de linhas entre gabarito clean e preparado: {diff_vs_clean}")
    

def run_excluded(df_prepared):

    excluded_status = {"pending", "canceled"}

    df_excluded = df_prepared[df_prepared["order_status"].isin(excluded_status)].copy()

    output_path = os.path.join(QUALITY_DIR, "vendas_excluidas.csv")

    df_excluded.to_csv(output_path, index=False)

    print(f"Arquivo excluido salvo em: {output_path}")

    print(f"Total de linhas no dataset excluído: {len(df_excluded)}")

    return df_excluded


def run_financial(df_prepared):

    financial_status = {"paid", "returned"}

    df_financial = df_prepared[df_prepared["order_status"].isin(financial_status)].copy()

    output_path = os.path.join(ANALYTICS_DIR, "vendas_financeiras.csv")

    df_financial.to_csv(output_path, index=False)

    print(f"Arquivo financeiro salvo em: {output_path}")

    print(f"Total de linhas no dataset financeiro: {len(df_financial)}")

    return df_financial


def run_inconsistent(df_raw):

    df = df_raw.copy()

    financial_status = {"paid", "returned"}

    df = df[df["order_status"].isin(financial_status)].copy()

    df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")

    df["unit_price"] = pd.to_numeric(df["unit_price"], errors="coerce")

    df["discount_pct"] = pd.to_numeric(df["discount_pct"], errors="coerce")


    invalid_quantity = df["quantity"].isna() | (df["quantity"] <= 0)
    invalid_unit_price = df["unit_price"].isna() | (df["unit_price"] <=0)
    invalid_discount_pct = df["discount_pct"].isna() | (df["discount_pct"] < 0) | (df["discount_pct"] > 1)
    
    inconsistent_mask = (invalid_quantity | invalid_unit_price | invalid_discount_pct)

    df_inconsistent = df[inconsistent_mask]
    
    return df_inconsistent


def validate_numeric_column(
    df,
    column,
    min_value=None,
    max_value=None,
    strictly_positive=False
    ):
    """Valida uma coluna numérica e remove valores inválidos."""

    df[column] = pd.to_numeric(df[column], errors="coerce")

    invalid = df[column].isna()

    if strictly_positive:
        invalid |= df[column] <= 0

    if min_value is not None:
        invalid |= df[column] < min_value

    if max_value is not None:
        invalid |= df[column] > max_value

    df = df[~invalid].copy()

    return df


def validate_text_column(df, column):
    normalized = df[column].astype(str).str.strip().str.lower()

    invalid = normalized.isna()
    invalid |= normalized == ""
    invalid |= normalized == "nan"

    df_valid = df[~invalid].copy()
    df_valid[column] = normalized[~invalid]

    return df_valid


def validate_date_column(df, column):
    """Valida coluna de datas, removendo valores inválidos."""

    # Tenta converter para datetime; erros viram NaT
    converted = pd.to_datetime(df[column], errors="coerce")

    invalid = converted.isna()

    df_valid = df[~invalid].copy()

    # Atualiza coluna com valores convertidos
    df_valid[column] = converted[~invalid]

    return df_valid


def validate_time_column(df, column):
    """Valida coluna de horários no formato HH:MM, removendo valores inválidos."""
    
    converted = pd.to_datetime(df[column], format="%H:%M", errors="coerce").dt.time

    valid = converted.notna()

    df = df[valid].copy()

    df[column] = converted[valid]

    return df


def clean_raw_sales(df_raw):
    """Aplicar regras básicas de limpeza no df_raw e retornar um DataFradme preparado."""
    
    # df_raw.copy() cria uma cópia independente desses dados. 
    # Iportante para não alterar diretamente a variável df_raw.
    df = df_raw.copy()

    df = validate_date_column(df, "order_date")
    df = validate_time_column(df, "order_time")
    
    df = validate_numeric_column(df, "quantity", strictly_positive=True)
    df = validate_numeric_column(df, "unit_price", strictly_positive=True)
    df = validate_numeric_column(df, "discount_pct", min_value=0, max_value=1)

    df = validate_text_column(df, "order_status")
    df = validate_text_column(df, "customer_id")
    df = validate_text_column(df, "customer_city")

    return df


def ensure_db_schema(conn):
    
    """Garantir que a tabela vendas exista aplicando o DDL."""
    base_dir = Path(__file__).resolve().parents[2]

    ddl_files = [
        base_dir / "sql" / "ddl" / "00_drop_legacy_tables.sql",
        base_dir / "sql" / "ddl" / "01_create_table_vendas.sql",
        base_dir / "sql" / "ddl" / "02_create_table_vendas_inconsistentes.sql",
        base_dir / "sql" / "views" / "analytics" / "vw_analytics_faturamento_mensal.sql",
        base_dir / "sql" / "views" / "quality" / "vw_quality_vendas_excluidas.sql",
        base_dir / "sql" / "views" / "analytics" /  "vw_analytics_vendas_financeiras.sql",
        base_dir / "sql" / "views"/ "analytics" /  "vw_analytics_faturamento_por_cidades.sql",
        base_dir / "sql" / "views"/ "analytics" /  "vw_analytics_ticket_medio.sql",
        base_dir / "sql" / "views" / "quality" / "vw_quality_financeiras_inconsistentes.sql",
        base_dir / "sql" / "views" / "analytics" /  "vw_analytics_produtos_mais_vendidos.sql",
        base_dir / "sql" / "views" / "kpis" /  "vw_kpis_resultado_liquido_final.sql",
        base_dir / "sql" / "views" / "kpis" /  "vw_kpis_resultado_financeiro.sql",
        base_dir / "sql" / "views" / "kpis" / "vw_kpis_resultado_total_v_excluidas.sql",
        base_dir / "sql" / "views" / "base" / "vw_base_vendas_financeiras.sql",
        base_dir / "sql" / "views" / "analytics" / "vw_analytics_categoria_mais_vendida.sql",
        base_dir / "sql" / "views"/ "analytics" / "vw_analytics_categorias_retornadas.sql",
        base_dir / "sql" / "views"/ "time_analysis" / "vw_time_analysis_vendas_hora.sql",
    ]

    for ddl_path in ddl_files:
        with open(ddl_path, "r", encoding="utf8") as f:
            conn.executescript(f.read())


def print_vendas_row_count():
    """Imprimir no terminal quantas linhas existem na tabela vendas do banco."""

    # Abre uma **conexão** com o mesmo banco que o pipeline usa:
    #`DB_PATH` → `data/processed/loja_rapida.db`.
    conn = sqlite3.connect(DB_PATH)

    #`cursor` é o objeto que o SQLite usa para: executar comandos SQL (`SELECT`, `INSERT`, etc.),
    # acessar os resultados das consultas.
    cursor = conn.cursor()

    # Me diga quantas linhas existem na tabela vendas.
    cursor.execute("SELECT COUNT(*) FROM vendas")

    # Consultar Notion Fase D - 4. Carga de dados 
    row_count = cursor.fetchone()[0]

    print(f"Total de linhas na tabela 'vendas': {row_count}")

    conn.close()


if __name__ == "__main__":

    # Ela chama a função run_raw_pipeline() somente quando o arquivo pipeline_vendas.py 
    # for executado diretamente no terminal.
    run_raw_pipeline()
    
    print_vendas_row_count()

import pandas as pd

from src.pipelines.pipeline_vendas import validate_numeric_column
from src.pipelines.pipeline_vendas import validate_text_column
from src.pipelines.pipeline_vendas import validate_date_column
from src.pipelines.pipeline_vendas import validate_time_column
from src.pipelines.pipeline_vendas import clean_raw_sales
from datetime import time
def test_validate_numeric_column_strictly_positive():
    df = pd.DataFrame({
        "quantity": [10, 0, -3, "abc", 5],
        "order_status": ["paid", "pending", "pending", "pending", "paid" ]   
        })
    
    result = validate_numeric_column(
    df,
    column="quantity",
    strictly_positive=True
    )

    assert result.loc[result["order_status"] == "paid", "quantity"].tolist() == [10, 5]


def test_validate_text_column_removes_empty_and_null():
    df = pd.DataFrame({
        "order_status": ["paid", "", None, "  ", "pending"]
    })

    result = validate_text_column(df, "order_status")

    assert len(result) == 2
    assert result["order_status"].tolist() == ["paid", "pending"]


def test_validate_numeric_column_min_and_max():
    df = pd.DataFrame({
        "discount_pct": [0.6, -0.2, 1.5],
        "order_status": ["paid", "pending", "pending"]
        })

    result = validate_numeric_column(
    df,
    column="discount_pct",
    min_value=0.5,
    max_value=1
    )    
    
    
    assert result.loc[result["order_status"] == "paid", "discount_pct"].tolist() == [0.6]



def test_validate_date_column():
    df = pd.DataFrame({
        "order_date": [
            "2024-11-01",
            "invalid-date",
            None,
            "2024-11-05"
        ]
    })

    result = validate_date_column(df, "order_date")

    assert len(result) == 2
    assert pd.api.types.is_datetime64_any_dtype(result["order_date"])

def test_validate_time_column():
    df = pd.DataFrame({
        "order_time": ["10:30", "25:99", None, "08:15"]
    })

    result = validate_time_column(df, "order_time")

    assert len(result) == 2
    assert result["order_time"].tolist() == [time(10, 30), time(8, 15)]

def test_clean_raw_sales_full_flow():
    df = pd.DataFrame({
        "order_date": ["2024-11-01", "invalid"],
        "order_time": ["10:00", "99:99"],
        "quantity": [2, -1],
        "unit_price": [10.0, 0],
        "discount_pct": [0.1, 1.5,],
        "order_status": ["paid", "pending"],
        "customer_id": ["C001", None],
        "customer_city": ["São Paulo", None]
    })

    result = clean_raw_sales(df)

    # Apenas a primeira linha deve sobreviver
    assert (result["order_status"] == "paid").any()
    assert not ((result["order_status"] == "pending") & (result["quantity"] <= 0)).any()


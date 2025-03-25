import pandas as pd
from django.db.models import Avg, Min, Max
from analysis.models import PatientTest
from datetime import datetime

def get_longitudinal_trends():
    # Query all test records
    test_records = PatientTest.objects.values("test_type__name", "date_taken", "result")

    # Convert queryset to DataFrame
    df = pd.DataFrame(list(test_records))

    if df.empty:
        return {"error": "No test data available."}

    # Convert date to Year-Month format
    df["date_taken"] = pd.to_datetime(df["date_taken"]).dt.to_period("M")
    
    # Convert result to numeric
    df["result"] = pd.to_numeric(df["result"], errors="coerce")

    # Aggregate by Test Type and Date
    trends = df.groupby(["test_type__name", "date_taken"]).agg(
        avg_result=("result", "mean"),
        min_result=("result", "min"),
        max_result=("result", "max")
    ).reset_index()

    # Convert to JSON-friendly format
    trends["date_taken"] = trends["date_taken"].astype(str)
    result_dict = trends.groupby("test_type__name").apply(lambda x: x.to_dict(orient="records")).to_dict()

    return result_dict

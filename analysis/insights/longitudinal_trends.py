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

    # Convert date to datetime and bucket into 6-month intervals
    df["date_taken"] = pd.to_datetime(df["date_taken"])
    df["date_bucket"] = df["date_taken"].dt.to_period("6M")  # Every 6 months

    # Convert result to numeric
    df["result"] = pd.to_numeric(df["result"], errors="coerce")

    # Aggregate by Test Type and Date Bucket
    trends = df.groupby(["test_type__name", "date_bucket"]).agg(
        avg_result=("result", "mean"),
        min_result=("result", "min"),
        max_result=("result", "max")
    ).reset_index()

    # Convert date_bucket to string for JSON compatibility
    trends["date_bucket"] = trends["date_bucket"].astype(str)
    
    # Convert to JSON-friendly format
    result_dict = trends.groupby("test_type__name").apply(lambda x: x.to_dict(orient="records")).to_dict()

    return result_dict

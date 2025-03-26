import pandas as pd
from analysis.models import PatientTest

def get_test_correlation():
    # Query all test records including patient id, test type, and result
    qs = PatientTest.objects.values("patient_id", "test_type__name", "result")
    df = pd.DataFrame(list(qs))
    
    if df.empty:
        return {"error": "No test data available."}
    
    # Ensure test result is numeric
    df["result"] = pd.to_numeric(df["result"], errors="coerce")
    
    # Group by patient and test type: compute the average test result per patient for each test
    pivot_df = df.groupby(["patient_id", "test_type__name"])["result"].mean().reset_index()
    
    # Pivot the table: index=patient_id, columns=test_type, values=average result
    pivot_table = pivot_df.pivot(index="patient_id", columns="test_type__name", values="result")
    
    # Compute the correlation matrix across test types
    corr_matrix = pivot_table.corr()
    
    # Convert the correlation matrix to a dictionary for JSON serialization
    return corr_matrix.to_dict()

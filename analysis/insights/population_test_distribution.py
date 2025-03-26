import pandas as pd
import numpy as np
from analysis.models import PatientTest

def get_population_test_distribution():
    # Query all test records with test name and result
    test_records = PatientTest.objects.values("test_type__name", "result")
    
    # Convert queryset to DataFrame
    df = pd.DataFrame(list(test_records))
    
    if df.empty:
        return {"error": "No test data available."}
    
    # Ensure result is numeric
    df["result"] = pd.to_numeric(df["result"], errors="coerce")
    
    distribution_data = {}
    
    # Loop through each test type
    for test in df["test_type__name"].unique():
        test_df = df[df["test_type__name"] == test]
        # Drop NaN values
        results = test_df["result"].dropna()
        if results.empty:
            continue
        # Create 10 bins for the distribution
        counts, bin_edges = np.histogram(results, bins=10)
        # Prepare data for JSON (lists of counts and bin edge labels)
        # We'll create labels like "low - high" for each bin
        labels = []
        for i in range(len(bin_edges)-1):
            labels.append(f"{round(bin_edges[i],2)} - {round(bin_edges[i+1],2)}")
        
        distribution_data[test] = {
            "labels": labels,
            "counts": counts.tolist()
        }
    
    return distribution_data

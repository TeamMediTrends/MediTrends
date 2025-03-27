import numpy as np
import pandas as pd
from django.core.serializers.json import DjangoJSONEncoder
from ..models import PatientTest, TestType  

def get_patient_test_levels():
    """Get the average test levels for each patient and each test."""
    # Load patient test data including test names
    patient_tests = PatientTest.objects.select_related('test_type').values("patient_id", "test_type__name", "test_type_id", "result")
    
    df = pd.DataFrame(patient_tests)
    df['result'] = pd.to_numeric(df['result'], errors='coerce')
    df.columns = df.columns.str.strip()

    # Check if the data contains the necessary columns
    if df.empty:
        return {"error": "No patient test data available."}
    
    # Pivot data to have test types as columns and patients as rows
    df_pivot = df.pivot_table(index="patient_id", columns="test_type_id", values="result", aggfunc="mean").fillna(0)

    # Generate a dictionary of the results (this will be used for plotting)
    test_data = []
    for test_type_id in df_pivot.columns:
        test_name = df[df['test_type_id'] == test_type_id].iloc[0]['test_type__name']
        test_data.append({
            'test_type_id': test_type_id,
            'test_name': test_name,  # Add the test name here
            'levels': df_pivot[test_type_id].tolist()
        })

    return {"test_data": test_data}

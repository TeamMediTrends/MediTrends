import os
import django
import numpy as np
from datetime import datetime

# Set the Django settings module and initialize Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "MediTrends.settings")
django.setup()

from analysis.models import Patient, TestType, PatientTest, AnomalousTestResult

# Define the valid ranges for each test type (from seed_patient_tests.py)
TEST_RANGES = {
    "complete blood count (cbc)": (4.0, 10.0, "x10^9/L"),
    "red blood cells (rbc)": (4.2, 5.9, "x10^12/L"),
    "liver enzymes": (7, 56, "U/L"),
    "total protein": (6.0, 8.3, "g/dL"),
    "white blood cells (wbc)": (4.0, 11.0, "x10^9/L"),
    "hemoglobin -(hgb)": (12.0, 17.5, "g/dL"),
    "cholesterol": (120, 200, "mg/dL"),
    "triglycerides": (50, 150, "mg/dL"),
    "platelets": (150, 450, "x10^9/L"),
    "thyroid stimulating hormone": (0.4, 4.0, "mIU/L"),
    "glucose": (70, 110, "mg/dL"),
    "a1c": (4.0, 6.5, "%"),
    "calcium": (8.5, 10.5, "mg/dL"),
    "vitamin d": (20, 50, "ng/mL"),
    "sodium": (135, 145, "mmol/L"),
    "c- reactive protein (crp)": (0, 10, "mg/L"),
    "potassium": (3.5, 5.2, "mmol/L"),
    "chloride": (96, 106, "mmol/L"),
    "CO2": (23, 29, "mmol/L"),
    "blood urea nitrogen (bun)": (7, 20, "mg/dL"),
    "creatinine": (0.6, 1.3, "mg/dL"),
}

def calculate_and_seed_anomalies():
    all_anomaly_records = []  # List to hold AnomalousTestResult instances

    # Process each test type
    test_types = TestType.objects.all()
    for test_type in test_types:
        test_name = test_type.name.lower()
        
        # Skip if no valid range is defined for this test type
        if test_name not in TEST_RANGES:
            continue

        min_val, max_val, unit = TEST_RANGES[test_name]

        # Get all test results for this test type
        test_results_qs = PatientTest.objects.filter(test_type=test_type)
        if not test_results_qs.exists():
            continue

        # Convert test results to float values (skip non-numeric)
        test_results = []
        for test in test_results_qs:
            try:
                test_results.append(float(test.result))
            except ValueError:
                print(f"Skipping non-numeric test result '{test.result}' for patient {test.patient.id}")
                continue

        if not test_results:
            continue

        # Calculate the average and standard deviation
        average = sum(test_results) / len(test_results)
        std_dev = np.std(test_results)

        # Calculate thresholds using 90% of the distance from the average to the valid range boundaries
        below_offset = (average - min_val) * 0.9
        below_threshold = average - below_offset
        above_offset = (max_val - average) * 0.9
        above_threshold = average + above_offset

        print(f"\nTest Type: {test_type.name}")
        print(f"  Valid range: {min_val} to {max_val} {unit}")
        print(f"  Average: {average:.2f}")
        print(f"  Std Dev: {std_dev:.2f}")
        print(f"  Below threshold: {below_threshold:.2f} (offset: {below_offset:.2f})")
        print(f"  Above threshold: {above_threshold:.2f} (offset: {above_offset:.2f})")

        # Identify anomalies and prepare records to seed the database
        for test in test_results_qs:
            try:
                result_value = float(test.result)
            except ValueError:
                continue

            if result_value < below_threshold or result_value > above_threshold:
                # Calculate a simple deviation score based on the difference from the threshold
                if result_value < below_threshold:
                    deviation_score = below_threshold - result_value
                else:
                    deviation_score = result_value - above_threshold

                # Create an anomaly record instance
                anomaly_record = AnomalousTestResult(
                    patient_id=test.patient.id,
                    test_type=test.test_type.name,
                    test_value=result_value,
                    mean=average,
                    std_dev=std_dev,
                    deviation_score=deviation_score
                )
                all_anomaly_records.append(anomaly_record)
                print(f"  Anomaly: Patient {test.patient.id} - Result: {result_value} "
                    f"({'Below' if result_value < below_threshold else 'Above'} threshold)")
    
    # Seed the anomalies into the database if any are found
    if all_anomaly_records:
        AnomalousTestResult.objects.bulk_create(all_anomaly_records)
        print(f"\nSeeded {len(all_anomaly_records)} anomalies into the database.")
    else:
        print("\nNo anomalies detected.")

if __name__ == "__main__":
    calculate_and_seed_anomalies()

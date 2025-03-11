import random
from datetime import datetime, timedelta
from django.utils.timezone import make_aware
from django.db import transaction
from analysis.models import Patient, TestType, PatientTest

# Define realistic ranges and units for each test type
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

# Get all patients and test types
patients = Patient.objects.all()
test_types = TestType.objects.all()

# Start date and time interval (one month apart)
start_date = datetime(2019, 1, 1)
time_interval = timedelta(days=30)  # Approximate monthly interval

test_records = []

with transaction.atomic():
    for patient in patients:
        for i in range(60):  # 60 months (5 years)
            test_date = make_aware(start_date + i * time_interval)
            for test_type in test_types:
                test_name = test_type.name.lower()
                
                # Get valid range and unit
                if test_name in TEST_RANGES:
                    min_val, max_val, unit = TEST_RANGES[test_name]
                    result_value = round(random.uniform(min_val, max_val), 2)
                else:
                    result_value = round(random.uniform(50, 200), 2)
                    unit = "N/A"

                test_records.append(PatientTest(
                    patient=patient,
                    test_type=test_type,
                    result=str(result_value),
                    unit=unit,
                    date_taken=test_date
                ))

    # Bulk insert into the database
    PatientTest.objects.bulk_create(test_records)

print(f"Successfully added {len(test_records)} patient test records.")

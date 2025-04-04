import json
from django.http import JsonResponse
from analysis.models import Patient, PatientTest
from datetime import date

def get_demographics(filters):
    try:
        if not isinstance(filters, dict) or not filters:
            return {
                "error": "Invalid filters provided."
            }

        print(f"Received filters in API: {filters}")
        patients = Patient.objects.all()
        
        today = date.today()

        # Process filters
        for key, value in filters.items():
            if key in ["smoking", "alcohol", "drugs", "religious", "overweight"]:
                # Boolean filters: Convert to True if selected, otherwise don't include
                if value == "true":  # only include key if value is "true"
                    patients = patients.filter(**{key: True})

            elif key in ["ethnicity", "state", "marital_status", "sex", "dependents", "education_level", "insurance_status"]:
                patients = patients.filter(**{key: value})
                
            elif key == "income":
                # Handle income classes
                if "Lower income" in value:
                    patients = patients.filter(income__gte=0, income__lte=25000)
                if "Lower middle" in value:
                    patients = patients.filter(income__gte=25000, income__lte=50000)
                if "Middle class" in value:
                    patients = patients.filter(income__gte=50000, income__lte=100000)
                if "Upper middle class" in value:
                    patients = patients.filter(income__gte=100000, income__lte=200000)
            # Handle age filtering using min_age and max_age directly
            elif key == "min_age":
                min_age = int(value)
                # Patient must be at least min_age years old: born on or before today minus min_age years.
                max_birth_date = date(today.year - min_age, today.month, today.day)
                patients = patients.filter(dob__lte=max_birth_date)
            elif key == "max_age":
                max_age = int(value)
                # Patient must be no older than max_age: born on or after today minus max_age years.
                min_birth_date = date(today.year - max_age, today.month, today.day)
                patients = patients.filter(dob__gte=min_birth_date)
        # Get the selected patient IDs and calculate the percentage
        patient_ids = patients.values_list("id", flat=True)
        total_patients = Patient.objects.count()
        selected_percentage = round((len(patient_ids) / total_patients) * 100, 2) if total_patients > 0 else 0

        # Get test results for selected patients
        test_results = PatientTest.objects.filter(patient_id__in=patient_ids).values("date_taken", "test_type__name", "result")

        # Structure data for visualization
        data = {}
        for entry in test_results:
            test_name = entry["test_type__name"]
            date = entry["date_taken"].strftime("%Y-%m")
            result = float(entry["result"])

            if test_name not in data:
                data[test_name] = {}
            if date not in data[test_name]:
                data[test_name][date] = []
            data[test_name][date].append(result)

        # Compute average test values per month
        for test_name, dates in data.items():
            for date, values in dates.items():
                data[test_name][date] = sum(values) / len(values)

        return {
            "test_data": data,
            "selected_percentage": selected_percentage,
            "selected_criteria": filters
        }

    except Exception as e:
        print(f"Unexpected error: {e}")
        return {"error": "Something went wrong on the server."}


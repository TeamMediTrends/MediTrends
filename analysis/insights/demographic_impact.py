import json
from django.http import JsonResponse
from analysis.models import Patient, PatientTest, TestType

def get_demographics(filters):
    """Fetch patients matching the selected demographic criteria."""
    patients = Patient.objects.all()

    # Apply filters dynamically based on user selections
    for key, value in filters.items():
        if key == "income":
            min_income, max_income = value
            patients = patients.filter(income__gte=min_income, income__lte=max_income)
        elif key == "dependents":
            min_dep, max_dep = value
            patients = patients.filter(dependents__gte=min_dep, dependents__lte=max_dep)
        else:
            patients = patients.filter(**{key: value})

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

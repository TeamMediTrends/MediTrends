import json
from analysis.models import Patient, PatientTest

def get_demographics(filters):
    try:
        if not isinstance(filters, dict) or not filters:
            return {
                "error": "Invalid filters provided."
            }

        patients = Patient.objects.all()
        for key, value in filters.items():
            if key == "sex":
                patients = patients.filter(sex=value)  # Apply sex filter

        patient_ids = patients.values_list("id", flat=True)
        total_patients = Patient.objects.count()
        selected_percentage = round((len(patient_ids) / total_patients) * 100, 2) if total_patients > 0 else 0

        # Get test results for selected patients
        test_results = PatientTest.objects.filter(patient_id__in=patient_ids).values("date_taken", "test_type__name", "result")

        # Structure data for visualization
        data = []
        for entry in test_results:
            test_name = entry["test_type__name"]
            date = entry["date_taken"].strftime("%Y-%m-%d")
            result = float(entry["result"])
            data.append({
                "test_type": test_name,
                "date_taken": date,
                "result": result
            })

        return {
            "test_data": data,
            "selected_percentage": selected_percentage,
            "selected_criteria": filters
        }

    except Exception as e:
        return {"error": str(e)}

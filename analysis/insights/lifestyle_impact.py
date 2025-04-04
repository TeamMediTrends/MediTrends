import pandas as pd
from django.db.models import Count
from datetime import datetime
from analysis.models import Patient

def get_age_distribution():
    """
    Calculates the age distribution using the following bins:
    18-25, 25-35, 35-45, 45-55, 55-65, and 65+.
    """
    current_year = datetime.now().year
    # Define age bins and labels
    age_bins = [18, 25, 35, 45, 55, 65, float("inf")]
    age_labels = ["18-25", "25-35", "35-45", "45-55", "55-65", "65+"]
    
    # Get all patients and compute their ages
    patients = Patient.objects.all()
    ages = [current_year - patient.dob.year for patient in patients if patient.dob]
    
    # Initialize counts for each bin
    distribution = {label: 0 for label in age_labels}
    for age in ages:
        for i in range(len(age_bins) - 1):
            if age_bins[i] <= age < age_bins[i+1]:
                distribution[age_labels[i]] += 1
                break

    num_patients = len(ages)
    # Convert counts to percentages
    percentage_distribution = {label: round((count / num_patients) * 100, 2) 
                            for label, count in distribution.items()}
    return percentage_distribution

def percentage_distribution(queryset, field):
    """
    Computes a percentage distribution for a given field.
    """
    num_patients = Patient.objects.count()
    distribution = queryset.values(field).annotate(count=Count("id"))
    return {entry[field]: round((entry["count"] / num_patients) * 100, 2) for entry in distribution}

def get_demographic_percentages():
    num_patients = Patient.objects.count()
    if num_patients == 0:
        return {"error": "No patients available."}
    
    # Use our custom age distribution function
    age_distribution = get_age_distribution()
    
    # Compute percentages for other demographics
    state_distribution = percentage_distribution(Patient.objects, "state")
    sex_distribution = percentage_distribution(Patient.objects, "sex")
    ethnicity_distribution = percentage_distribution(Patient.objects, "ethnicity")
    insurance_distribution = percentage_distribution(Patient.objects, "insurance_status")
    education_distribution = percentage_distribution(Patient.objects, "education_level")
    pre_existing_distribution = percentage_distribution(Patient.objects, "pre_existing_conditions")
    marital_distribution = percentage_distribution(Patient.objects, "marital_status")
    dependents_distribution = percentage_distribution(Patient.objects, "dependents")
    physical_disability_distribution = percentage_distribution(Patient.objects, "disabled_physically")
    smoking_distribution = percentage_distribution(Patient.objects, "smoking")
    alcohol_distribution = percentage_distribution(Patient.objects, "alcohol")
    drug_distribution = percentage_distribution(Patient.objects, "drugs")
    overweight_distribution = percentage_distribution(Patient.objects, "overweight")
    
    return {
        "Distribution by Age": age_distribution,
        "Distribution by State": state_distribution,
        "Distribution by Sex": sex_distribution,
        "Distribution by Ethnicity": ethnicity_distribution,
        "Distribution by Insurance Status": insurance_distribution,
        "Distribution by Education Level": education_distribution,
        "Distribution by Pre-existing Conditions": pre_existing_distribution,
        "Distribution by Marital Status": marital_distribution,
        "Distribution by Number of Dependents": dependents_distribution,
        "Distribution by Physical Disability": physical_disability_distribution,
        "Distribution by Smoking Status": smoking_distribution,
        "Distribution by Alcohol Status": alcohol_distribution,
        "Distribution by Drug Status": drug_distribution,
        "Distribution by Weight Status": overweight_distribution,
    }

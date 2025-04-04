import pandas as pd
from django.db.models import Count
from analysis.models import Patient
from django.db.models import Q

def get_income_demographics():
    # Define income classes as tuples: (Label, minimum income, maximum income)
    # These income classes categorize patients into different income brackets.
    income_classes = [
        ("Lower income", 0, 25000),
        ("Lower middle", 25000, 50000),
        ("Middle class", 50000, 100000),
        ("Upper middle class", 100000, 200000),
    ]

    # Calculate overall income distribution for patients with a non-null income
    # Exclude patients with null income values to ensure accurate calculations.
    patients_with_income = Patient.objects.exclude(income__isnull=True)
    total_patients = patients_with_income.count()
    
    # Initialize a dictionary to store the percentage distribution of patients across income classes.
    income_distribution = {}
    for label, min_inc, max_inc in income_classes:
        # Count patients in each income class and calculate their percentage.
        count = patients_with_income.filter(income__gte=min_inc, income__lt=max_inc).count()
        income_distribution[label] = round((count / total_patients) * 100, 2) if total_patients > 0 else 0

    # Demographic factors to analyze
    # These fields represent various demographic attributes of patients.
    demographics = {
        "Sex": "sex",
        "Education": "education_level",
        "Insurance": "insurance_status",
        "Religious": "religious",
        "Smoking": "smoking",
        "Alcohol": "alcohol",
        "Drugs": "drugs",
        "Overweight": "overweight",
    }

    # For each demographic factor, for each income class, calculate distribution percentages.
    # This section analyzes how demographic factors vary across income classes.
    income_impact = {}
    for demo_label, field in demographics.items():
        income_impact[demo_label] = {}
        for label, min_inc, max_inc in income_classes:
            # Filter patients within the current income class.
            qs = patients_with_income.filter(income__gte=min_inc, income__lt=max_inc)
            total_in_class = qs.count()
            if total_in_class > 0:
                # Annotate the count of each demographic value within the income class.
                distribution = qs.values(field).annotate(count=Count("id"))
                # Calculate the percentage distribution for each demographic value.
                demo_distribution = {
                    entry[field]: round((entry["count"] / total_in_class) * 100, 2)
                    for entry in distribution
                }
                # Store the overall percentage and demographic distribution for the income class.
                income_impact[demo_label][label] = {
                    "overall": income_distribution[label],
                    "distribution": demo_distribution,
                }
            else:
                # Handle cases where no patients fall into the income class.
                income_impact[demo_label][label] = {
                    "overall": income_distribution[label],
                    "distribution": {},
                }

    # Return the overall income distribution and the demographic impact by income class.
    return {
        "income_distribution": income_distribution,
        "income_impact": income_impact,
    }

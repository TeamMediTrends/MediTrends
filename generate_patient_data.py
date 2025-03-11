import pandas as pd
import random
from datetime import datetime, timedelta

n = 50  # Number of patients

# Sample data lists
first_names = ["John", "Jane", "Alice", "Bob", "Charlie", "David", "Eva", "Frank", "Grace", "Hannah", "Ian", "Jill", "Kevin", "Laura", "Mike", "Nina", "Oscar", "Pam", "Quincy", "Rachel"]
last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Miller", "Davis", "Garcia", "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson", "Thomas", "Taylor", "Moore", "Jackson", "Martin"]
states = ["CA", "NY", "TX", "FL", "IL", "PA", "OH", "MI", "GA", "NC"]
ethnicities = ["Caucasian", "African American", "Hispanic", "Asian", "Other"]
marital_statuses = ["Single", "Married", "Divorced", "Widowed"]
sexes = ["M", "F", "O"]
education_levels = ["High School", "Associate", "Bachelor", "Master", "Doctorate"]
insurance_statuses = ["Insured", "Uninsured"]

# Function to generate a random date between two dates
def random_date(start, end):
    delta = end - start
    random_days = random.randint(0, delta.days)
    return start + timedelta(days=random_days)

start_date = datetime(1950, 1, 1)
end_date = datetime(2005, 12, 31)

# Create the simulated data dictionary
data = {
    "First Name": [random.choice(first_names) for _ in range(n)],
    "Last Name": [random.choice(last_names) for _ in range(n)],
    "DOB": [random_date(start_date, end_date).strftime("%Y-%m-%d") for _ in range(n)],
    "State": [random.choice(states) for _ in range(n)],
    "Ethnicity": [random.choice(ethnicities) for _ in range(n)],
    "Income": [round(random.uniform(20000, 120000), 2) for _ in range(n)],
    "Marital Status": [random.choice(marital_statuses) for _ in range(n)],
    "Dependents": [random.randint(0, 5) for _ in range(n)],
    "Pre-existing Conditions": [random.choice([True, False]) for _ in range(n)],
    "Sex": [random.choice(sexes) for _ in range(n)],
    "Education Level": [random.choice(education_levels) for _ in range(n)],
    "Disabled Mentally": [random.choice([True, False]) for _ in range(n)],
    "Disabled Physically": [random.choice([True, False]) for _ in range(n)],
    "Insurance Status": [random.choice(insurance_statuses) for _ in range(n)],
    "Religious": [random.choice([True, False]) for _ in range(n)],
    "Smoking": [random.choice([True, False]) for _ in range(n)],
    "Alcohol": [random.choice([True, False]) for _ in range(n)],
    "Drugs": [random.choice([True, False]) for _ in range(n)],
    "Overweight": [random.choice([True, False]) for _ in range(n)]
}

# Create a DataFrame and save it to Excel
df = pd.DataFrame(data)
file_path = "sample_patients_50.xlsx"
df.to_excel(file_path, index=False)
print("Excel file saved to:", file_path)

from django.db import models

class Medication(models.Model):
    name = models.CharField(max_length=100)  # Medication name
    dosage = models.IntegerField()  # Dosage in mg
    last_filled = models.DateField()  # Last filled date

class Patient(models.Model):
    """ Stores patient information. """
    SEX_CHOICES = [('M', 'Male'), ('F', 'Female'), ('O', 'Other')]
    MARITAL_STATUS_CHOICES = [('Single', 'Single'), ('Married', 'Married'),
                            ('Divorced', 'Divorced'), ('Widowed', 'Widowed')]
    EDUCATION_LEVEL_CHOICES = [('High School', 'High School'), ('Associate', 'Associate'),
                            ('Bachelor', 'Bachelor'), ('Master', 'Master'), ('Doctorate', 'Doctorate')] 
    
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    dob = models.DateField()
    state = models.CharField(max_length=2)
    ethnicity = models.CharField(max_length=50, blank=True, null=True)
    income = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    marital_status = models.CharField(max_length=10, choices=MARITAL_STATUS_CHOICES, blank=True, null=True)
    dependents = models.IntegerField(default=0)
    pre_existing_conditions = models.BooleanField(default=False)
    sex = models.CharField(max_length=1, choices=SEX_CHOICES)
    education_level = models.CharField(max_length=12, choices=EDUCATION_LEVEL_CHOICES, blank=True, null=True)
    disabled_mentally = models.BooleanField(default=False)
    disabled_physically = models.BooleanField(default=False)
    insurance_status = models.CharField(max_length=50, blank=True, null=True)
    religious = models.BooleanField(default=False)
    smoking = models.BooleanField(default=False)
    alcohol = models.BooleanField(default=False)
    drugs = models.BooleanField(default=False)
    overweight = models.BooleanField(default=False)

class TestType(models.Model):
    """ Stores different types of medical tests. """
    name = models.CharField(max_length=100, unique=True)

class PatientTest(models.Model):
    """ Stores test results for a specific patient. """
    patient = models.ForeignKey('Patient', on_delete=models.CASCADE)
    test_type = models.ForeignKey(TestType, on_delete=models.CASCADE)
    result = models.CharField(max_length=50) 
    unit = models.CharField(max_length=20, blank=True, null=True) 
    date_taken = models.DateField()
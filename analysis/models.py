from django.db import models

class Medication(models.Model):
    name = models.CharField(max_length=100)  # Medication name
    dosage = models.IntegerField()  # Dosage in mg
    last_filled = models.DateField()  # Last filled date


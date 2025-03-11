from django.contrib import admin
from .models import Medication, Patient, TestType, PatientTest

admin.site.register(Medication)
admin.site.register(Patient)
admin.site.register(TestType)
admin.site.register(PatientTest)
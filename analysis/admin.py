from django.contrib import admin
from .models import Patient, TestType, PatientTest

admin.site.register(Patient)
admin.site.register(TestType)
admin.site.register(PatientTest)
from django.contrib import admin
from .models import Patient, TestType, PatientTest, AnomalousTestResult

admin.site.register(Patient)
admin.site.register(TestType)
admin.site.register(PatientTest)
admin.site.register(AnomalousTestResult)
from django.shortcuts import render

from .models import Medication

def med_list(request):
    meds = Medication.objects.all()  # Get all meds from the database
    return render(request, 'medications.html', {'meds': meds})

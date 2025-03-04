from django.shortcuts import render
from django.views.generic import ListView

from ..models import Medication

# def med_list(request):
#     meds = Medication.objects.all()  # Get all meds from the database
#     return render(request, 'analysis/medications.html', {'meds': meds})

class MedicationListView(ListView):
    model = Medication
    template_name = 'analysis/medications.html'
    context_object_name = 'meds'
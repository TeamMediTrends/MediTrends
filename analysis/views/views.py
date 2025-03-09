from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import ListView, TemplateView

from ..models import Medication

class HomeView(TemplateView):
    template_name = 'analysis/home.html'
    context_object_name = 'home'

class MedicationListView(LoginRequiredMixin, ListView):
    model = Medication
    template_name = 'analysis/medications.html'
    context_object_name = 'meds'
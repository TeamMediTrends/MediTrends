from django.views.generic import ListView
from django.shortcuts import get_object_or_404
from django import forms
from django.utils.timezone import datetime
from .models import Patient, PatientTest, TestType

class UploadFileForm(forms.Form):
    file = forms.FileField()

class TestTypeForm(forms.ModelForm):
    class Meta:
        model = TestType
        fields = ['name']

class TestFilterForm(forms.Form):
    test_type = forms.ModelChoiceField(
        queryset=TestType.objects.all(),
        required=False,
        label="Test Type"
    )
    start_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'}),
        label="Start Date"
    )
    end_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'}),
        label="End Date"
    )

class PatientTestListView(ListView):
    """Displays and filters test results for a patient."""
    template_name = "patients/patient_tests.html"
    context_object_name = "tests"

    def get_queryset(self):
        patient = get_object_or_404(Patient, pk=self.kwargs['pk'])
        tests = PatientTest.objects.filter(patient=patient)

        # Get filter parameters
        test_type = self.request.GET.get("test_type")
        start_date = self.request.GET.get("start_date")
        end_date = self.request.GET.get("end_date")

        # Apply filters
        if test_type:
            tests = tests.filter(test_type_id=test_type)
        if start_date:
            tests = tests.filter(date_taken__gte=start_date)
        if end_date:
            tests = tests.filter(date_taken__lte=end_date)

        return tests

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        patient = get_object_or_404(Patient, pk=self.kwargs['pk'])
        context["patient"] = patient
        context["form"] = TestFilterForm(self.request.GET)  # Prefill form with current filter values
        return context
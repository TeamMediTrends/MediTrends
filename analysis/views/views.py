from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from ..mixins import AdminRequiredMixin
from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView, TemplateView, FormView, CreateView, DetailView
from django.urls import reverse_lazy
import pandas as pd
from ..forms import UploadFileForm, TestTypeForm, TestFilterForm
from ..models import Patient, TestType, PatientTest


class HomeView(TemplateView):
    """Home page view"""
    template_name = "analysis/home.html"
    content_object_name = "home"


class UploadPatientsView(LoginRequiredMixin, AdminRequiredMixin, FormView):
    """Handles patient data upload via Excel file"""
    template_name = "patients/upload.html"
    form_class = UploadFileForm
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        """Process the uploaded Excel file and create Patient records"""
        excel_file = self.request.FILES["file"]
        try:
            df = pd.read_excel(excel_file, engine="openpyxl")
            print("DataFrame head:\n", df.head())


            patients = [
                Patient(
                    first_name=row["First Name"],
                    last_name=row["Last Name"],
                    dob=row["DOB"],
                    state=row["State"],
                    ethnicity=row.get("Ethnicity", ""),
                    income=row.get("Income", 0),
                    marital_status=row.get("Marital Status", ""),
                    dependents=row.get("Dependents", 0),
                    pre_existing_conditions=row.get("Pre-existing Conditions", False),
                    sex=row["Sex"],
                    education_level=row.get("Education Level", ""),
                    disabled_mentally=row.get("Disabled Mentally", False),
                    disabled_physically=row.get("Disabled Physically", False),
                    insurance_status=row.get("Insurance Status", ""),
                    religious=row.get("Religious", False),
                    smoking=row.get("Smoking", False),
                    alcohol=row.get("Alcohol", False),
                    drugs=row.get("Drugs", False),
                    overweight=row.get("Overweight", False),
                )
                for _, row in df.iterrows()
            ]
            Patient.objects.bulk_create(patients)

            return super().form_valid(form)

        except Exception as e:
            print("Error processing the file:", e)
            return self.form_invalid(form) 

    def get_context_data(self, **kwargs):
        """Ensures the form context is correctly passed"""
        context = super().get_context_data(**kwargs)
        context["form"] = self.get_form()
        return context

class TestTypeListView(LoginRequiredMixin, ListView):
    """Displays a list of all test types."""
    model = TestType
    template_name = "test_types/test_type_list.html"
    context_object_name = "test_types"

class AddTestTypeView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    """Allows users to add a new test type."""
    model = TestType
    form_class = TestTypeForm
    template_name = "test_types/add_test_type.html"
    success_url = reverse_lazy("test_type_list")

class PatientListView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    """Displays a list of all patients."""
    model = Patient
    template_name = "patients/patient_list.html"
    context_object_name = "patients"

class PatientDetailView(LoginRequiredMixin, AdminRequiredMixin, DetailView):
    """Displays detailed information about a specific patient."""
    model = Patient
    template_name = "patients/patient_detail.html"
    context_object_name = "patient"

class PatientTestListView(LoginRequiredMixin, AdminRequiredMixin, ListView):
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
        context["form"] = TestFilterForm(self.request.GET)
        return context

class ReportCreatorView(LoginRequiredMixin, TemplateView):
    """Displays the report creator page."""
    template_name = "analysis/report_creator.html"
    context_object_name = "report_creator"

class InsightsView(LoginRequiredMixin, TemplateView):
    """Displays the insights page."""
    template_name = "analysis/insights/insights.html"
    context_object_name = "insights"

class LongitudinalTrendsView(LoginRequiredMixin, TemplateView):
    """Displays the page for longitudinal trends analysis."""
    template_name = "analysis/insights/longitudinal_trends.html"
    context_object_name = "longitudinal_trends"

class PopulationTestDistributionView(LoginRequiredMixin, TemplateView):
    """Displays the page for population test distribution analysis."""
    template_name = "analysis/insights/population_test_distribution.html"
    context_object_name = "population_test_distribution"

class TestCorrelationView(LoginRequiredMixin, TemplateView):
    """Displays the page for test correlation analysis."""
    template_name = "analysis/insights/test_correlation.html"
    context_object_name = "test_correlation"

class PatientClusteringView(LoginRequiredMixin, TemplateView):
    """Displays the page for patient clustering analysis."""
    template_name = "analysis/insights/patient_clustering.html"
    context_object_name = "patient_clustering"

class DemographicImpactView(LoginRequiredMixin, TemplateView):
    """Displays the page for demographic impact analysis."""
    template_name = "analysis/insights/demographic_impact.html"
    context_object_name = "demographic_impact"

class TestAnomaliesView(LoginRequiredMixin, TemplateView):
    """Displays the page for test anomalies analysis."""
    template_name = "analysis/insights/test_anomalies.html"
    context_object_name = "test_anomalies"

class SeasonalVariationsView(LoginRequiredMixin, TemplateView):
    """Displays the page for seasonal variations analysis."""
    template_name = "analysis/insights/seasonal_variations.html"
    context_object_name = "seasonal_variations"

class TestForecastingView(LoginRequiredMixin, TemplateView):
    """Displays the page for test forecasting analysis."""
    template_name = "analysis/insights/test_forecasting.html"
    context_object_name = "test_forecasting"

class LifestyleImpactView(LoginRequiredMixin, TemplateView):
    """Displays the page for lifestyle impact analysis."""
    template_name = "analysis/insights/lifestyle_impact.html"
    context_object_name = "lifestyle_impact"

class PreexistingConditionsView(LoginRequiredMixin, TemplateView):
    """Displays the page for preexisting conditions analysis."""
    template_name = "analysis/insights/preexisting_conditions.html"
    context_object_name = "preexisting_conditions"

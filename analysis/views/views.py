from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import ListView, TemplateView, FormView, CreateView
from django.urls import reverse_lazy
import pandas as pd
from ..forms import UploadFileForm, TestTypeForm
from ..models import Patient, Medication, TestType


class HomeView(TemplateView):
    """Home page view"""
    template_name = "analysis/home.html"


class MedicationListView(LoginRequiredMixin, ListView):
    """List of medications"""
    model = Medication
    template_name = "analysis/medications.html"
    context_object_name = "meds"


class UploadPatientsView(LoginRequiredMixin, FormView):
    """Handles patient data upload via Excel file"""
    template_name = "analysis/upload.html"
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

class AddTestTypeView(LoginRequiredMixin, CreateView):
    """Allows users to add a new test type."""
    model = TestType
    form_class = TestTypeForm
    template_name = "test_types/add_test_type.html"
    success_url = reverse_lazy("test_type_list")
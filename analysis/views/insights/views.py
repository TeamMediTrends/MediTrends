from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from ...mixins import AdminRequiredMixin
from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView, TemplateView, FormView, CreateView, DetailView
from django.views import View
from django.urls import reverse_lazy
from datetime import date
import pandas as pd
import json
from ...models import Patient, TestType, PatientTest, AnomalousTestResult
from analysis.insights.longitudinal_trends import get_longitudinal_trends
from analysis.insights.population_test_distribution import get_population_test_distribution
from analysis.insights.test_correlation import get_test_correlation
from analysis.insights.patient_clustering import get_patient_test_levels
from analysis.insights.demographic_impact import get_demographics
from analysis.insights.lifestyle_impact import get_demographic_percentages
from analysis.insights.income_demographics import get_income_demographics


class InsightsView(LoginRequiredMixin, TemplateView):
    """Displays the insights page."""
    template_name = "analysis/insights/insights.html"
    context_object_name = "insights"

class LongitudinalTrendsPageView(LoginRequiredMixin, TemplateView):
    template_name = "analysis/insights/longitudinal_trends.html"

class LongitudinalTrendsView(LoginRequiredMixin, View):
    """Class-based view to fetch longitudinal trends of patient test data."""

    def get(self, request, *args, **kwargs):
        data = get_longitudinal_trends()
        return JsonResponse(data, safe=False)

class PopulationTestDistributionView(LoginRequiredMixin, TemplateView):
    """Displays the page for population test distribution analysis."""
    template_name = "analysis/insights/population_test_distribution.html"
    context_object_name = "population_test_distribution"

class PopulationTestDistributionAPIView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        data = get_population_test_distribution()
        return JsonResponse(data, safe=False)

class TestCorrelationView(LoginRequiredMixin, TemplateView):
    """Displays the page for test correlation analysis."""
    template_name = "analysis/insights/test_correlation.html"
    context_object_name = "test_correlation"

class TestCorrelationAPIView(LoginRequiredMixin, View):
    """API view that returns the correlation matrix as JSON."""
    def get(self, request, *args, **kwargs):
        data = get_test_correlation()
        return JsonResponse(data, safe=False)

class PatientClusteringView(LoginRequiredMixin, TemplateView):
    """Displays the page for patient clustering analysis."""
    template_name = "analysis/insights/patient_clustering.html"
    context_object_name = "patient_clustering"

class PatientTestLevelsApiView(View):
    """API View to fetch test levels for all patients."""
    def get(self, request, *args, **kwargs):
        data = get_patient_test_levels()
        return JsonResponse(data, safe=False)
    
class TestAnomaliesView(LoginRequiredMixin, TemplateView):
    template_name = "analysis/insights/test_anomalies.html"

class TestAnomaliesAPIView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        anomalies = list(AnomalousTestResult.objects.all().values())
        return JsonResponse(anomalies, safe=False)

class LifestyleImpactView(LoginRequiredMixin, TemplateView):
    template_name = "analysis/insights/lifestyle_impact.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["demographics"] = get_demographic_percentages()
        return context
    
class IncomeDemographicsView(TemplateView):
    template_name = "analysis/insights/income_demographics.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["income_data"] = get_income_demographics()
        return context

class DemoPageView(TemplateView):
    template_name = "analysis/insights/demo.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class DemoFilterResultsView(View):
    def get(self, request):
        filters = json.loads(request.GET.get("filters", "{}"))

        queryset = PatientTest.objects.all()

        # If filtering by sex, first get patient IDs
        if "sex" in filters:
            patient_ids = Patient.objects.filter(sex=filters["sex"]).values_list("id", flat=True)
            queryset = queryset.filter(patient_id__in=patient_ids)

        data = list(queryset.values("test_type", "date_taken", "result"))

        return JsonResponse({"test_data": data})

class DemographicImpactView(LoginRequiredMixin, TemplateView):
    """Displays the page for demographic impact analysis."""
    template_name = "analysis/insights/demographic_impact.html"

class DemographicImpactApiView(View):
    """API View to fetch test levels for selected demographic groups."""
    def get(self, request):
        filters = json.loads(request.GET.get("filters", "{}"))
                
        queryset = PatientTest.objects.all()

        # Apply filters based on provided criteria in the filters dictionary
        if "smoking" in filters:
            patient_ids = Patient.objects.filter(smoking=filters["smoking"]).values_list("id", flat=True)
            queryset = queryset.filter(patient_id__in=patient_ids)

        if "overweight" in filters:
            patient_ids = Patient.objects.filter(overweight=filters["overweight"]).values_list("id", flat=True)
            queryset = queryset.filter(patient_id__in=patient_ids)

        if "religious" in filters:
            patient_ids = Patient.objects.filter(religious=filters["religious"]).values_list("id", flat=True)
            queryset = queryset.filter(patient_id__in=patient_ids)

        if "pre_existing_conditions" in filters:
            patient_ids = Patient.objects.filter(pre_existing_conditions=filters["pre_existing_conditions"]).values_list("id", flat=True)
            queryset = queryset.filter(patient_id__in=patient_ids)

        if "alcohol" in filters:
            patient_ids = Patient.objects.filter(alcohol=filters["alcohol"]).values_list("id", flat=True)
            queryset = queryset.filter(patient_id__in=patient_ids)

        if "drugs" in filters:
            patient_ids = Patient.objects.filter(drugs=filters["drugs"]).values_list("id", flat=True)
            queryset = queryset.filter(patient_id__in=patient_ids)
            
            # Handling state filter - support multiple states
        if "state" in filters:
            patient_ids = Patient.objects.filter(state__in=filters["state"]).values_list("id", flat=True)
            queryset = queryset.filter(patient_id__in=patient_ids)
            
        if "sex" in filters:
            patient_ids = Patient.objects.filter(sex__in=filters["sex"]).values_list("id", flat=True)
            queryset = queryset.filter(patient_id__in=patient_ids)
            
        if "marital_status" in filters:
            patient_ids = Patient.objects.filter(marital_status__in=filters["marital_status"]).values_list("id", flat=True)
            queryset = queryset.filter(patient_id__in=patient_ids)
            
        if "education_level" in filters:
            patient_ids = Patient.objects.filter(education_level__in=filters["education_level"]).values_list("id", flat=True)
            queryset = queryset.filter(patient_id__in=patient_ids)
            
        if "ethnicity" in filters:
            patient_ids = Patient.objects.filter(ethnicity__in=filters["ethnicity"]).values_list("id", flat=True)
            queryset = queryset.filter(patient_id__in=patient_ids)
            
        if "dependents" in filters:
            patient_ids = Patient.objects.filter(dependents__in=filters["dependents"]).values_list("id", flat=True)
            queryset = queryset.filter(patient_id__in=patient_ids)
            
        if "insurance_status" in filters:
            patient_ids = Patient.objects.filter(insurance_status__in=filters["insurance_status"]).values_list("id", flat=True)
            queryset = queryset.filter(patient_id__in=patient_ids)
            
        if "income" in filters:
            income_ranges = {
                "Lower income": (0, 25000),
                "Lower middle": (25000, 50000),
                "Middle class": (50000, 100000),
                "Upper middle class": (100000, 200000)
            }
            for label, (min_inc, max_inc) in income_ranges.items():
                if label in filters["income"]:
                    patient_ids = Patient.objects.filter(income__gte=min_inc, income__lte=max_inc).values_list("id", flat=True)
                    queryset = queryset.filter(patient_id__in=patient_ids)
        
        if "min_age" in filters:
            min_age = int(filters["min_age"])
            today = date.today()
            max_birth_date = date(today.year - min_age, today.month, today.day)
            patient_ids = Patient.objects.filter(dob__lte=max_birth_date).values_list("id", flat=True)
            queryset = queryset.filter(patient_id__in=patient_ids)
            
        if "max_age" in filters:
            max_age = int(filters["max_age"])
            today = date.today()
            min_birth_date = date(today.year - max_age, today.month, today.day)
            patient_ids = Patient.objects.filter(dob__gte=min_birth_date).values_list("id", flat=True)
            queryset = queryset.filter(patient_id__in=patient_ids)
                
        # If no filters are applied, return all test results
        if not filters:
            queryset = PatientTest.objects.all()
            
        data = []
        for test in queryset:
            data.append({
                "test_type": test.test_type.name,  # ✅ this gets the name instead of the ID
                "date_taken": test.date_taken,
                "result": test.result,
            })

        data_count = len(data)
        patient_count = data_count / 1260
        patient_percentage = (patient_count / 55) * 100

        return JsonResponse({"test_data": data, "patient_percentage": patient_percentage})

from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from ...mixins import AdminRequiredMixin
from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView, TemplateView, FormView, CreateView, DetailView
from django.views import View
from django.urls import reverse_lazy
import pandas as pd
from ...forms import UploadFileForm, TestTypeForm, TestFilterForm
from ...models import Patient, TestType, PatientTest
from analysis.insights.longitudinal_trends import get_longitudinal_trends


class InsightsView(LoginRequiredMixin, TemplateView):
    """Displays the insights page."""
    template_name = "analysis/insights/insights.html"
    context_object_name = "insights"

class LongitudinalTrendsPageView(TemplateView):
    template_name = "analysis/insights/longitudinal_trends.html"

class LongitudinalTrendsView(View):
    """Class-based view to fetch longitudinal trends of patient test data."""

    def get(self, request, *args, **kwargs):
        data = get_longitudinal_trends()
        return JsonResponse(data, safe=False)

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

from django.urls import path
from .views.views import HomeView, UploadPatientsView, TestTypeListView, AddTestTypeView, PatientListView, PatientDetailView, PatientTestListView, ReportCreatorView
from .views.insights.views import InsightsView, LongitudinalTrendsPageView, LongitudinalTrendsView, PopulationTestDistributionView, PopulationTestDistributionAPIView, TestCorrelationView, TestCorrelationAPIView, PatientClusteringView, PatientTestLevelsApiView, DemographicImpactView, DemographicImpactApiView, TestAnomaliesView, SeasonalVariationsView, TestForecastingView, LifestyleImpactView, PreexistingConditionsView
from django.contrib.auth.views import LogoutView
from django.shortcuts import render

# Logout page view
def logout_page(request):
    return render(request, "registration/logout.html")

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("upload/", UploadPatientsView.as_view(), name="upload_patients"), 
    path('test-types/', TestTypeListView.as_view(), name='test_type_list'),
    path('test-types/add/', AddTestTypeView.as_view(), name='add_test_type'),
    path('patients/', PatientListView.as_view(), name='patient_list'),
    path('patients/<int:pk>/', PatientDetailView.as_view(), name='patient_detail'),
    path('patients/<int:pk>/tests/', PatientTestListView.as_view(), name='patient_tests'),
    path("logout/", logout_page, name="logout_page"),
    path("accounts/logout/", LogoutView.as_view(), name="logout"),
    path("insights/", InsightsView.as_view(), name="insights"),
    path("insights/longitudinal-trends/", LongitudinalTrendsPageView.as_view(), name="longitudinal_trends_page"),
    path("insights/population-test-distribution/", PopulationTestDistributionView.as_view(), name="population_test_distribution"),
    path("insights/test-correlation/", TestCorrelationView.as_view(), name="test_correlation"),
    path("insights/patient-clustering/", PatientClusteringView.as_view(), name="patient_clustering"),
    path("insights/demographic-impact/", DemographicImpactView.as_view(), name="demographic_impact"),
    path("test-anomalies/", TestAnomaliesView.as_view(), name="test_anomalies"),
    path("seasonal-variations/", SeasonalVariationsView.as_view(), name="seasonal_variations"),
    path("test-forecasting/", TestForecastingView.as_view(), name="test_forecasting"),
    path("lifestyle-impact/", LifestyleImpactView.as_view(), name="lifestyle_impact"),
    path("preexisting-conditions/", PreexistingConditionsView.as_view(), name="preexisting_conditions"),
    path("report-creator/", ReportCreatorView.as_view(), name="report_creator"),
    path('api/longitudinal-trends/', LongitudinalTrendsView.as_view(), name='longitudinal_trends_api'),
    path("api/population-test-distribution/", PopulationTestDistributionAPIView.as_view(), name="population_test_distribution_api"),
    path("api/test-correlation/", TestCorrelationAPIView.as_view(), name="test_correlation_api"),
    path("api/patient-test-levels/", PatientTestLevelsApiView.as_view(), name="patient_test_levels_api"),
    path("api/demographic-impact/", DemographicImpactApiView.as_view(), name="demographic_impact_api"),

    
]

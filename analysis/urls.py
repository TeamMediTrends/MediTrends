from django.urls import path
from .views.views import HomeView, UploadPatientsView, TestTypeListView, AddTestTypeView, PatientListView, PatientDetailView, PatientTestListView, InsightFindingsView, ReportCreatorView, InsightReportsView, InsightsView
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
    path("insight-findings/", InsightFindingsView.as_view(), name="insight_findings"),
    path("insight-reports/", InsightReportsView.as_view(), name="insight_reports"),
    path("report-creator/", ReportCreatorView.as_view(), name="report_creator"),
]

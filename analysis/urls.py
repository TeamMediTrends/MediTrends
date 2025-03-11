from django.urls import path
from .views.views import MedicationListView, HomeView, UploadPatientsView, TestTypeListView, AddTestTypeView

urlpatterns = [
    path("medications/", MedicationListView.as_view(), name="medications"),
    path("", HomeView.as_view(), name="home"),
    path("upload/", UploadPatientsView.as_view(), name="upload_patients"), 
    path('test-types/', TestTypeListView.as_view(), name='test_type_list'),
    path('test-types/add/', AddTestTypeView.as_view(), name='add_test_type'),
]

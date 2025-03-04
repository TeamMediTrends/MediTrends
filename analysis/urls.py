from django.urls import path
from .views.views import MedicationListView

urlpatterns = [
    path('medications/', MedicationListView.as_view(), name='med_list'),
]
from django.urls import path
from .views.views import MedicationListView
from .views.views import HomeView

urlpatterns = [
    path('medications/', MedicationListView.as_view(), name='medications'),
    path('home/', HomeView.as_view(), name='home'),
]
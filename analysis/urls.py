from django.urls import path
from .views.views import med_list

urlpatterns = [
    path('medications/', med_list, name='med_list'),
]
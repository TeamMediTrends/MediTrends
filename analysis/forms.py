from django import forms
from .models import TestType

class UploadFileForm(forms.Form):
    file = forms.FileField()

class TestTypeForm(forms.ModelForm):
    class Meta:
        model = TestType
        fields = ['name']


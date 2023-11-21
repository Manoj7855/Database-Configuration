from django import forms
from .models import Registerform

class MyRegisterform(forms.ModelForm):
    class Meta:
        model= Registerform
        fields=["name","age","address","contact","email"]
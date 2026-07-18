from django import forms
from .models import Salary


class SalaryForm(forms.ModelForm):
    class Meta:
        model = Salary
        fields = ['employee', 'month', 'basic_salary', 'hra', 'da', 'bonus']
        widgets = {
            'employee': forms.Select(attrs={'class': 'form-select'}),
            'month': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'July 2026'}),
            'basic_salary': forms.NumberInput(attrs={'class': 'form-control'}),
            'hra': forms.NumberInput(attrs={'class': 'form-control'}),
            'da': forms.NumberInput(attrs={'class': 'form-control'}),
            'bonus': forms.NumberInput(attrs={'class': 'form-control'}),
        }

from django import forms
from .models import Company, Vacancy, Resume, Application


class CreateCompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        exclude = ['slug', 'user']


class CreateVacancyForm(forms.ModelForm):
    class Meta:
        model = Vacancy
        exclude = ['slug', 'user', 'company']


class CreateResumeForm(forms.ModelForm):
    class Meta:
        model = Resume
        exclude = ['slug', 'user']


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        exclude = ['user', 'vacancy']

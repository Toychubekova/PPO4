from django import forms
from .models import Salary_employees

class SalaryYearMonthForm(forms.ModelForm):
    class Meta:
        model = Salary_employees
        fields = ('year', 'month', 'general_amount')

    def __init__(self, *args, **kwargs):
        super(SalaryYearMonthForm, self).__init__(*args, **kwargs)
        self.fields['year'].widget.attrs['readonly'] = True
        self.fields['month'].widget.attrs['readonly'] = True

class SalaryFormFilter(forms.Form):
    start_date = forms.DateField(required=False, widget=forms.TextInput(attrs={'type': 'date'}))
    end_date = forms.DateField(required=False, widget=forms.TextInput(attrs={'type': 'date'}))
from django import forms
from .models import Employees, Positions

from employees.models import Salary

class EmployeeForm(forms.ModelForm):

    class Meta:
        model = Employees
        fields = ('Full_Name', 'Position', 'Salary', 'Address', 'Phone')

        def __init__(self, *args, **kwargs):
            super(EmployeeForm, self).__init__(*args, **kwargs)
            # Добавим выпадающий список для поля 'position'
            self.fields['Position'] = forms.ModelChoiceField(queryset=Positions.objects.all(), to_field_name='id')
def _get_month_name(month_number: int) -> str:
    if month_number == 1:
         return "January"
    elif month_number == 2:
        return "February"
    elif month_number == 3:
        return "March"
    elif month_number == 4:
        return "April"
    elif month_number == 5:
        return "May"
    elif month_number == 6:
        return "June"
    elif month_number == 7:
        return "July"
    elif month_number == 8:
        return "August"
    elif month_number == 9:
        return "September"
    elif month_number == 10:
        return "October"
    elif month_number == 11:
        return "November"
    elif month_number == 12:
        return "December"


class SelectYearMonthForm(forms.Form):
    year_choices = [(None, '----------')] + [(i, i) for i in range(2023, 2101)]
    year = forms.ChoiceField(choices=year_choices, label='Year')

    month_choices = [(None, '----------')] + [(i, _get_month_name(i)) for i in range(1, 13)]
    month = forms.ChoiceField(choices=month_choices, label='Month')


class SalaryForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(SalaryForm, self).__init__(*args, **kwargs)

        self.fields['year'].widget.attrs['readonly'] = True
        self.fields['month'].widget.attrs['readonly'] = True

    class Meta:
        model = Salary
        fields = ['year', 'month', 'employee', 'general']

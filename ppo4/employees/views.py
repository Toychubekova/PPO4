from django.shortcuts import render, get_object_or_404, redirect

from django.views.generic import ListView, UpdateView, View
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import Sum
from employees.models import Employees, Salary
from employees.salary_method.salary import SalaryService
from budget.models import Budget

from employees.forms import EmployeeForm, SelectYearMonthForm, SalaryForm


def list(request):
    employees = Employees.objects.all()
    return render(request, 'list.html', {'employees': employees})

def detail(request, pk):
    employee = get_object_or_404(Employees, pk=pk)
    return render(request, 'detail.html', {'employee': employee})

def create(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            employee = form.save(commit=False)
            employee.save()
            return redirect('list')  # Перенаправление на страницу списка сотрудников
    else:
        form = EmployeeForm()
    return render(request, 'form.html', {'form': form})

def edit(request, pk):
    employee = get_object_or_404(Employees, pk=pk)
    if request.method == 'POST':
        form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            employee = form.save(commit=False)
            employee.save()
            return redirect('list')  # Перенаправление на страницу списка сотрудников
    else:
        form = EmployeeForm(instance=employee)
    return render(request, 'edit.html', {'form': form, 'employee': employee})

def delete(request, pk):
    employee = get_object_or_404(Employees, pk=pk)
    employee.delete()
    return redirect('list')

class ListSalaryView(ListView):
    model = Salary
    template_name = 'salary-list.html'
    context_object_name = 'salaries'

    def get(self, request, *args, **kwargs):
        year = request.session.get('year')
        month = request.session.get('month')

        context = self.get_context_data(year=year, month=month)
        request.session['total_sum'] = context['total_sum']

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        year: int = request.POST.get('year')
        month: int = request.POST.get('month')

        request.session['year'] = year
        request.session['month'] = month

        SalaryService.create_salary_list(year, month)
        context = self.get_context_data(year=year, month=month)
        request.session['total_sum'] = context['total_sum']

        return render(request, self.template_name, context)

    def get_context_data(self, **kwargs):
        context: dict = {}
        year: int = kwargs['year']
        month: int = kwargs['month']

        context['salaries'] = SalaryService.get_salary_list(year, month)
        context['total_sum'] = context['salaries'].aggregate(total_sum=Sum('general'))['total_sum']
        context['choice_form'] = SelectYearMonthForm()
        context['is_issued'] = SalaryService.is_issued(context['salaries'])
        context['is_period_selected'] = bool(year and month)
        context['budget'] = Budget.objects.all().first().budget


        if year and month:
            context['choice_form'].initial = {'year': year, 'month': month}

        return context


class UpdateSalaryView(UpdateView):
    model = Salary
    template_name = 'salary-update.html'
    form_class = SalaryForm
    success_url = reverse_lazy('salary-index')


class IssueSalaryView(View):
    @staticmethod
    def get(request, *args, **kwargs):
        total_sum = request.session.get('total_sum')
        year: int = request.session.get('year')
        month: int = request.session.get('month')

        if Budget.objects.is_enough_budget(total_sum):
            SalaryService.issue_all(SalaryService.get_salary_list(year, month))
        else:
            messages.error(request, 'There is not enough budget to pay salaries to all employees')

        return redirect('salary-index')

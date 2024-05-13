from django.shortcuts import render, get_object_or_404, redirect
from employees.models import Employees, Salary
from .models import Salary_employees
from .forms import SalaryYearMonthForm
from django.db import connection
from django.contrib import messages
from datetime import datetime
from budget.models import Budget


def employee_salary_view(request):
    current_year = datetime.now().year
    current_month = datetime.now().month

    selected_year = request.GET.get('year', current_year)
    selected_month = request.GET.get('month', current_month)

    budget = Budget.objects.first()

    with connection.cursor() as cursor:
        cursor.execute("DECLARE @Total FLOAT; EXEC GetSalary @Year=%s, @Month=%s",[selected_year, selected_month])
        total = cursor.fetchone()
        if total is not None:
            total = total[0]

    years = [year for year in range(2020, 2300)]
    months = [
        (1, 'Январь'), (2, 'Февраль'), (3, 'Март'), (4, 'Апрель'),
        (5, 'Май'), (6, 'Июнь'), (7, 'Июль'), (8, 'Август'),
        (9, 'Сентябрь'), (10, 'Октябрь'), (11, 'Ноябрь'), (12, 'Декабрь')
    ]
    salaries = Salary_employees.objects.filter(year=selected_year, month=selected_month)
    employees = Employees.objects.all()
    is_issued = all(salary.is_given for salary in salaries)

    return render(request, 'salaries_list.html', {
        'salaries': salaries,
        'years': years,
        'months': months,
        'selected_year': selected_year,
        'selected_month': selected_month,
        'employees': employees,
        'total': total,
        'is_issued': is_issued,
        'budget': budget,
    })






def issue_unissued_salaries(request):
    if request.method == 'POST':
        year_str = request.POST.get('year')
        month_str = request.POST.get('month')

        if year_str and month_str:
            try:
                year = int(year_str)
                month = int(month_str)

                with connection.cursor() as cursor:
                    cursor.execute("DECLARE @Result INT; EXEC ToIssueSalaries @Year=%s, @Month=%s, @Result=@Result OUTPUT; SELECT @Result;", [year, month])
                    result = cursor.fetchone()[0]

                    if result == 1:
                        messages.success(request, 'Зарплаты успешно выданы')
                    elif result == 0:
                        messages.error(request, 'Ошибка: Не удалось выполнить операцию')
                    elif result == -1:
                        messages.error(request, 'Ошибка: Недостаточно средств в бюджете для выдачи зарплат')
                    else:
                        messages.error(request, 'Ошибка: Неизвестная ошибка')
            except Exception as e:
                messages.error(request, f' Выдано {e}')
        else:
            messages.error(request, 'Ошибка: Не выбран год или месяц')

    return redirect('employee_salary_view')

def salary_edit(request, pk):
    salary = get_object_or_404(Salary, pk=pk)
    if request.method == 'POST':
        form = SalaryYearMonthForm(request.POST, instance=salary)
        if form.is_valid():
            general = form.cleaned_data['general']
            try:
                with connection.cursor() as cursor:
                    cursor.execute("EXEC UpdateSalary @general=%s, @salaryID=%s", [pk, general])
            except Exception as e:
                pass
            return redirect('employees:employee_salary_view')
    else:
        form = SalaryYearMonthForm(instance=salary)
    return render(request, 'salaries_edit.html', {'form': form, 'salary': salary})

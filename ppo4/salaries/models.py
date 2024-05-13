from django.db import models
from employees.models import Employees

class Salary_employees(models.Model):
    year = models.IntegerField()
    month = models.IntegerField()
    employee = models.ForeignKey(Employees, on_delete=models.CASCADE)
    purchases = models.IntegerField()
    productions = models.IntegerField()
    sales = models.IntegerField()
    common_amount = models.IntegerField()
    base_salary = models.FloatField()
    bonus_amount = models.FloatField()
    general_amount = models.FloatField()
    is_given = models.BooleanField()

    class Meta:
        db_table = 'salaries'

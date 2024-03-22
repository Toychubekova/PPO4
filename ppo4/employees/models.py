from django.db import models
from positions.models import Positions




# Create your models here.
class Employees(models.Model):
    Full_Name = models.CharField(max_length=255, db_column='Full_Name')
    Position = models.ForeignKey(Positions, on_delete=models.CASCADE, db_column='Position')
    Salary = models.DecimalField(max_digits=19, decimal_places=2, db_column='Salary')
    Address = models.CharField(max_length=255, db_column='Address')
    Phone = models.CharField(max_length=15, db_column='Phone')

    class Meta:
        db_table = 'Employees'

    def __str__(self):
        return self.Full_Name

class Salary(models.Model):
    year = models.PositiveIntegerField('Год')
    month = models.PositiveIntegerField('Месяц')
    employee = models.ForeignKey(Employees,
                                 on_delete=models.PROTECT,
                                 related_name='salaries',
                                 verbose_name='Employee')
    procurements = models.PositiveIntegerField('Quantity of purchases')
    productions = models.PositiveIntegerField('Quantity of productions')
    sales = models.PositiveIntegerField('Quantity of sales')
    common = models.PositiveIntegerField('Total number of participations')
    bonus = models.FloatField('Bonus')
    general = models.PositiveIntegerField('To issue')
    is_issued = models.BooleanField('Issued', default=False)

    class Meta:
        verbose_name = 'Salary'
        unique_together = ('year', 'month', 'employee')

    def __str__(self):
        return f'{self.year} {self.month} {self.employee} {self.general} {self.is_issued}'

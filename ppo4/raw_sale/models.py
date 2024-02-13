from django.db import models
from rawmaterials.models import RawMaterials
from employees.models import Employees
from django import forms

class Budget(models.Model):
    quantity = models.FloatField('Sum of budget')

    class Meta:
        verbose_name = 'Budget'
        verbose_name_plural = 'Budgets'

    def __str__(self):
        return f'Budget: {self.quantity}'

class RawSale(models.Model):
    material = models.ForeignKey(RawMaterials,
                                 on_delete=models.PROTECT,
                                 related_name='raw_sales',
                                 verbose_name='Raw Materials'
                                 )
    quantity = models.FloatField('Quantity')
    amount = models.FloatField('Amount')
    date = models.DateTimeField('Date and time', auto_now_add=True)
    employees = models.ForeignKey(Employees,
                                 on_delete=models.PROTECT,
                                 related_name='raw_sales',
                                 verbose_name='Employees'
                                 )

    class Meta:
        verbose_name = 'Raw Sale'
        verbose_name_plural = 'Raw Sales'

    def __str__(self):
        return f'Raw Sale {self.id}'

    @property
    def formatted_date(self):
        return self.date.strftime('%d.%m.%Y %H:%M')

class MaterialPurchaseForm(forms.ModelForm):
    class Meta:
        model = RawSale
        fields = ['material', 'quantity', 'amount', 'employees']

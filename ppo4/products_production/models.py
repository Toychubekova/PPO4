# models.py
from django.db import models
from fproduct.models import Finishs
from employees.models import Employees

class Product_production(models.Model):
    product = models.ForeignKey(
        Finishs,
        on_delete=models.PROTECT,
        related_name='productions',
        verbose_name='Product'
    )
    quantity = models.FloatField('Quantity')
    amount = models.FloatField('Amount', default=0)
    date = models.DateTimeField('Date and time', auto_now_add=True)
    employees = models.ForeignKey(
        Employees,
        on_delete=models.PROTECT,
        related_name='produced_products',
        verbose_name='Employee'
    )

    class Meta:
        db_table = 'product_production'

    def __str__(self):
        return f'Product production {self.id}'


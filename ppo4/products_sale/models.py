from django.db import models

from fproduct.models import Finishs
from employees.models import Employees

class Product_sale(models.Model):
    product = models.ForeignKey(
        Finishs,
        on_delete=models.CASCADE,
        related_name='product_sale',
        verbose_name='Product'
    )
    quantity = models.FloatField('Quantity')
    amount = models.FloatField('Amount')
    date = models.DateTimeField('Date and time', auto_now_add=True)
    employees = models.ForeignKey(
        Employees,
        on_delete=models.PROTECT,
        related_name='sales',
        verbose_name='Employee'
    )

    class Meta:
        verbose_name = 'Sales of product'
        verbose_name_plural = 'Product sales'
        db_table = 'product_sale'  # Указываем желаемое имя таблицы в базе данных

    def __str__(self):
        return f'Sales of product {self.id}'

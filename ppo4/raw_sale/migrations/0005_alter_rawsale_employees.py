# Generated by Django 5.0.1 on 2024-04-02 14:51

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0002_salary'),
        ('raw_sale', '0004_budget_percentage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rawsale',
            name='employees',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='procurements', to='employees.employees', verbose_name='Employees'),
        ),
    ]

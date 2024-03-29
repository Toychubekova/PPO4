# Generated by Django 5.0.1 on 2024-03-05 14:39

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('employees', '0001_initial'),
        ('fproduct', '0002_alter_finishs_amount'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product_production',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.FloatField(verbose_name='Количество')),
                ('amount', models.FloatField(default=0, verbose_name='Сумма')),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='Дата и время')),
                ('employees', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='employees_product_production', to='employees.employees', verbose_name='Employee')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='product_production', to='fproduct.finishs', verbose_name='Продукт')),
            ],
            options={
                'verbose_name': 'Product manufacturing',
                'verbose_name_plural': 'Products manufacturing',
            },
        ),
    ]

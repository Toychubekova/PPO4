# Generated by Django 5.0.1 on 2024-04-26 19:54

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('employees', '0002_salary'),
    ]

    operations = [
        migrations.CreateModel(
            name='Salary_employees',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.IntegerField()),
                ('month', models.IntegerField()),
                ('purchases', models.IntegerField()),
                ('productions', models.IntegerField()),
                ('sales', models.IntegerField()),
                ('common_amount', models.IntegerField()),
                ('base_salary', models.FloatField()),
                ('bonus_amount', models.FloatField()),
                ('general_amount', models.FloatField()),
                ('is_given', models.BooleanField()),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='employees.employees')),
            ],
            options={
                'db_table': 'salaries',
            },
        ),
    ]
# Generated by Django 5.0.1 on 2024-02-19 07:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fproduct', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='finishs',
            name='Amount',
            field=models.FloatField(),
        ),
    ]

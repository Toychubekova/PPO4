# Generated by Django 5.0.1 on 2024-02-11 14:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budget', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='budget',
            name='bonus',
            field=models.PositiveSmallIntegerField(default=0, verbose_name='Бонус'),
            preserve_default=False,
        ),
    ]
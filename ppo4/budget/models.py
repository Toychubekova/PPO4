from django.db import models


class BudgetManager(models.Manager):
    @staticmethod
    def is_enough_budget(quantity: float) -> bool:
        try:
            budget = Budget.objects.get(id=1)
            return quantity <= budget.budget
        except Budget.DoesNotExist:
            return False

    @staticmethod
    def decrease_budget(quantity: float) -> bool:
        try:
            budget = Budget.objects.get(id=1)
            budget.budget -= quantity
            budget.save()
            return True
        except Budget.DoesNotExist:
            return False

    @staticmethod
    def increase_budget(quantity: float) -> bool:
        return BudgetManager.increase_budget(-quantity)


class Budget(models.Model):
    budget = models.FloatField('Budget')
    percent = models.FloatField('Extra_charge')
    bonus = models.PositiveSmallIntegerField('Bonus')

    objects = BudgetManager()

    class Meta:
        verbose_name = 'Budget'

    def __str__(self):
        return str(self.budget)

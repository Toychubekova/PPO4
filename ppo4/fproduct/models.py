from django.db import models
from unit.models import Unit

class Finishs(models.Model):
    Name = models.CharField(max_length=255)
    Unit_id = models.ForeignKey(Unit, on_delete=models.CASCADE, db_column='Unit_id')
    Quantity = models.FloatField()
    Amount = models.FloatField()

    class Meta:
        db_table = 'FProducts'

    def __str__(self):
        return self.Name

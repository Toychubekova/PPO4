from django.db import models
from fproduct.models import Finishs
from rawmaterials.models import RawMaterials

class Ingredients(models.Model):
    Product_id = models.ForeignKey(Finishs, on_delete=models.CASCADE, db_column='Product_id')
    Quantity = models.FloatField()
    RawMaterial_id = models.ForeignKey(RawMaterials, on_delete=models.CASCADE, db_column='RawMaterial_id')

    class Meta:
        db_table = 'Ingredients'
        # unique_together = ('Product_id', 'RawMaterial_id')
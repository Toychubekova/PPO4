from django import forms
from .models import RawMaterials

class RawMaterialsForm(forms.ModelForm):

    class Meta:
        model = RawMaterials
        fields = ('Name', 'Unit_id', 'Quantity', 'Amount')
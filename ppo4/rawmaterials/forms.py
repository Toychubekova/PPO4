from django import forms
from .models import RawMaterials

class RawMaterialsForm(forms.ModelForm):

    class Meta:
        model = RawMaterials
        fields = ('Name', 'Unit_id', 'Quantity', 'Amount')

    def __init__(self, *args, **kwargs):
        super(RawMaterialsForm, self).__init__(*args, **kwargs)
        self.fields['Quantity'].initial = 0
        self.fields['Amount'].initial = 0
        self.fields['Quantity'].widget.attrs['readonly'] = True
        self.fields['Amount'].widget.attrs['readonly'] = True
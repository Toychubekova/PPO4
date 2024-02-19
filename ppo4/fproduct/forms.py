from django import forms
from .models import Finishs

class FinishsForm(forms.ModelForm):

    class Meta:
        model = Finishs
        fields = ('Name', 'Unit_id', 'Quantity', 'Amount')

    def __init__(self, *args, **kwargs):
        super(FinishsForm, self).__init__(*args, **kwargs)
        self.fields['Amount'].initial = 0  # 'Amount' вместо 'amount'
        self.fields['Quantity'].initial = 0  # 'Quantity' вместо 'quantity'
        self.fields['Amount'].widget.attrs['readonly'] = True
        self.fields['Quantity'].widget.attrs['readonly'] = True

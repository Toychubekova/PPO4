from django import forms

from raw_sale.models import RawSale


class MaterialPurchaseForm(forms.ModelForm):
    class Meta:
        model = RawSale
        fields = '__all__'

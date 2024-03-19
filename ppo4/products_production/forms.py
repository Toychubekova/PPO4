from django import forms

from .models import Product_production


class Products_productionForm(forms.ModelForm):
    class Meta:
        model = Product_production
        exclude = ['amount']

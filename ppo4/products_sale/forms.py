from django import forms

from products_sale.models import Product_sale


class Products_saleForm(forms.ModelForm):
    class Meta:
        model = Product_sale
        exclude = ['amount']

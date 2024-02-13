from django.urls import path
from raw_sale.views import (MaterialPurchaseView, CreateMaterialPurchaseView)


app_name = 'raw_sale'

urlpatterns = [
    path('', MaterialPurchaseView.as_view(), name='index'),
    path('create/', CreateMaterialPurchaseView.as_view(), name='create'),
]
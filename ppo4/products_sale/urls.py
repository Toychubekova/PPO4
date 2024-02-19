from django.urls import path

from products_sale.views import Products_saleView, CreateProducts_saleView, UpdateProducts_saleView, DeleteProducts_saleView
app_name = 'products_sale'

urlpatterns = [
    path('', Products_saleView.as_view(), name='index'),
    path('create/', CreateProducts_saleView.as_view(), name='create'),
    path('update/<int:pk>/', UpdateProducts_saleView.as_view(), name='update'),
    path('delete/<int:pk>/', DeleteProducts_saleView.as_view(), name='delete')
]

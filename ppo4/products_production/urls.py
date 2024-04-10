from django.urls import path

from products_production.views import Products_productionView, CreateProducts_productionView, UpdateProducts_productionView, DeleteProducts_productionView

app_name = 'products_production'

urlpatterns = [
    path('', Products_productionView.as_view(), name='index'),
    path('create/', CreateProducts_productionView.as_view(), name='create'),
    path('update/<int:pk>/', UpdateProducts_productionView.as_view(), name='update'),
    path('delete/<int:pk>/', DeleteProducts_productionView.as_view(), name='delete'),
]

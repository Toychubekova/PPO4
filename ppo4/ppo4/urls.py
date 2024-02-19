
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('employees/', include('employees.urls')),
    path('positions/',include('positions.urls')),
    path('rawmaterials/',include('rawmaterials.urls')),
    path('unit/',include('unit.urls')),
    path('ingredients/',include('ingredients.urls')),
    path('raw_sale/',include('raw_sale.urls')),
    path('finish/',include('fproduct.urls')),
    path('raw_sale/', include('raw_sale.urls')),
    path('products_sale/', include('products_sale.urls')),

]

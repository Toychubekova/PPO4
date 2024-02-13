from django.urls import path
from . import views

urlpatterns = [
    path('', views.FProduct_list, name='FProduct_list'),
    path('<int:pk>/', views.FProduct_detail, name='FProduct_detail'),
    path('new/', views.FProduct_create, name='FProduct_create'),
    path('<int:pk>/edit/', views.FProduct_edit, name='FProduct_edit'),
    path('<int:pk>/delete/', views.FProduct_delete, name='FProduct_delete'),
]
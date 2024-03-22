
from . import views
from django.urls import path

from employees.views import (
                             ListSalaryView, UpdateSalaryView, IssueSalaryView)

urlpatterns = [
    path('', views.list, name='list'),
    path('<int:pk>/', views.detail, name='detail'),
    path('new/', views.create, name='create'),
    path('<int:pk>/edit/', views.edit, name='edit'),
    path('<int:pk>/delete/', views.delete, name='delete'),
    path('salary/', ListSalaryView.as_view(), name='salary-index'),
    path('salary/update/<int:pk>', UpdateSalaryView.as_view(), name='salary-update'),
    path('salary/issue-all', IssueSalaryView.as_view(), name='salary-issue')
]

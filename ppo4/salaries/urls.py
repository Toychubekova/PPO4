
from django.urls import path
from . import views
urlpatterns = [
    path('', views.employee_salary_view, name='salaries_list'),
    path('allissue/', views.issue_unissued_salaries, name='issue_unissued_salaries'),
    path('<int:pk>/edit/', views.salary_edit, name='salaries_edit'),
]


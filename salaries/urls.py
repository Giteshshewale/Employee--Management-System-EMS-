from django.urls import path
from . import views

app_name = 'salaries'

urlpatterns = [
    path('', views.salary_list, name='list'),
    path('add/', views.salary_add, name='add'),
]

from django.urls import path
from . import views

app_name = 'reports'

urlpatterns = [
    path('', views.reports_home, name='home'),
    path('export/employees/csv/', views.export_employees_csv, name='export_employees_csv'),
    path('export/employees/excel/', views.export_employees_excel, name='export_employees_excel'),
    path('export/employees/pdf/', views.export_employees_pdf, name='export_employees_pdf'),
    path('export/departments/csv/', views.export_department_csv, name='export_departments_csv'),
    path('export/attendance/csv/', views.export_attendance_csv, name='export_attendance_csv'),
    path('export/salary/csv/', views.export_salary_csv, name='export_salary_csv'),
]

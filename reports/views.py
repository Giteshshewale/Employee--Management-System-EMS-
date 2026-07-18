import csv
import io

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render

from accounts.decorators import admin_or_hr_required
from attendance.models import Attendance
from departments.models import Department
from employees.models import Employee
from salaries.models import Salary


@login_required
@admin_or_hr_required
def reports_home(request):
    return render(request, 'reports/reports.html')


@login_required
@admin_or_hr_required
def export_employees_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="employee_report.csv"'
    writer = csv.writer(response)
    writer.writerow(['Employee ID', 'Name', 'Department', 'Designation', 'Email', 'Phone', 'Salary', 'Status'])
    for e in Employee.objects.select_related('department').all():
        writer.writerow([
            e.employee_id, e.full_name, e.department.name if e.department else '',
            e.designation, e.email, e.phone, e.salary, e.get_status_display(),
        ])
    return response


@login_required
@admin_or_hr_required
def export_department_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="department_report.csv"'
    writer = csv.writer(response)
    writer.writerow(['Department', 'Total Employees'])
    for d in Department.objects.all():
        writer.writerow([d.name, d.employee_count])
    return response


@login_required
@admin_or_hr_required
def export_attendance_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="attendance_report.csv"'
    writer = csv.writer(response)
    writer.writerow(['Employee', 'Date', 'Status'])
    for a in Attendance.objects.select_related('employee').all():
        writer.writerow([a.employee.full_name, a.date, a.get_status_display()])
    return response


@login_required
@admin_or_hr_required
def export_salary_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="salary_report.csv"'
    writer = csv.writer(response)
    writer.writerow(['Employee', 'Month', 'Basic', 'HRA', 'DA', 'Bonus', 'Total'])
    for s in Salary.objects.select_related('employee').all():
        writer.writerow([s.employee.full_name, s.month, s.basic_salary, s.hra, s.da, s.bonus, s.total_salary])
    return response


@login_required
@admin_or_hr_required
def export_employees_excel(request):
    """
    Requires `openpyxl` (listed in requirements.txt).
    Run `pip install openpyxl` locally before using this view.
    """
    from openpyxl import Workbook

    wb = Workbook()
    ws = wb.active
    ws.title = 'Employees'
    ws.append(['Employee ID', 'Name', 'Department', 'Designation', 'Email', 'Phone', 'Salary', 'Status'])
    for e in Employee.objects.select_related('department').all():
        ws.append([
            e.employee_id, e.full_name, e.department.name if e.department else '',
            e.designation, e.email, e.phone, float(e.salary), e.get_status_display(),
        ])

    buffer = io.BytesIO()
    wb.save(buffer)
    buffer.seek(0)
    response = HttpResponse(
        buffer.read(),
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    )
    response['Content-Disposition'] = 'attachment; filename="employee_report.xlsx"'
    return response


@login_required
@admin_or_hr_required
def export_employees_pdf(request):
    """
    Requires `reportlab` (listed in requirements.txt).
    Run `pip install reportlab` locally before using this view.
    """
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import A4
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
    from reportlab.lib.styles import getSampleStyleSheet

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()
    elements = [Paragraph('Employee Report', styles['Title'])]

    data = [['ID', 'Name', 'Department', 'Designation', 'Status']]
    for e in Employee.objects.select_related('department').all():
        data.append([e.employee_id, e.full_name, e.department.name if e.department else '', e.designation, e.get_status_display()])

    table = Table(data, repeatRows=1)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0d6efd')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
    ]))
    elements.append(table)
    doc.build(elements)

    buffer.seek(0)
    response = HttpResponse(buffer.read(), content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="employee_report.pdf"'
    return response

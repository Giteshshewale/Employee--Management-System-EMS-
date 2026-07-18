from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404

from accounts.decorators import admin_or_hr_required
from departments.models import Department
from notifications.utils import create_notification
from .models import Employee
from .forms import EmployeeForm

PAGE_SIZE = 10


@login_required
def employee_list(request):
    # Module 5 - Search, Module 6 - Filter, Module 7 - Pagination
    employees = Employee.objects.select_related('department').all()

    # Employee-role users only ever see their own record
    if request.user.role == 'employee' and not request.user.is_superuser:
        employees = employees.filter(user=request.user)

    query = request.GET.get('q', '').strip()
    if query:
        employees = employees.filter(
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(employee_id__icontains=query) |
            Q(email__icontains=query) |
            Q(city__icontains=query) |
            Q(department__name__icontains=query)
        )

    department_id = request.GET.get('department', '')
    if department_id:
        employees = employees.filter(department_id=department_id)

    status = request.GET.get('status', '')
    if status:
        employees = employees.filter(status=status)

    paginator = Paginator(employees, PAGE_SIZE)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'departments': Department.objects.all(),
        'query': query,
        'selected_department': department_id,
        'selected_status': status,
    }
    return render(request, 'employees/list.html', context)


@login_required
@admin_or_hr_required
def employee_add(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST, request.FILES)
        if form.is_valid():
            employee = form.save()
            create_notification(request.user, f'Employee {employee.full_name} was added.')
            send_mail(
                subject='Welcome to the company!',
                message=f'Hi {employee.full_name}, welcome aboard! Your employee ID is {employee.employee_id}.',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[employee.email],
                fail_silently=True,
            )
            messages.success(request, 'Employee added successfully.')
            return redirect('employees:list')
    else:
        form = EmployeeForm()
    return render(request, 'employees/form.html', {'form': form, 'title': 'Add Employee'})


@login_required
def employee_detail(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    if request.user.role == 'employee' and not request.user.is_superuser and employee.user_id != request.user.id:
        messages.error(request, "You can only view your own profile.")
        return redirect('employees:list')
    return render(request, 'employees/detail.html', {'employee': employee})


@login_required
@admin_or_hr_required
def employee_update(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    if request.method == 'POST':
        form = EmployeeForm(request.POST, request.FILES, instance=employee)
        if form.is_valid():
            form.save()
            messages.success(request, 'Employee updated successfully.')
            return redirect('employees:detail', pk=employee.pk)
    else:
        form = EmployeeForm(instance=employee)
    return render(request, 'employees/form.html', {'form': form, 'title': 'Update Employee'})


@login_required
@admin_or_hr_required
def employee_delete(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    if request.method == 'POST':
        employee.delete()
        messages.success(request, 'Employee deleted successfully.')
        return redirect('employees:list')
    return render(request, 'employees/confirm_delete.html', {'employee': employee})

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from departments.models import Department
from employees.models import Employee
from leaves.models import Leave


@login_required
def dashboard_view(request):
    employees_qs = Employee.objects.all()

    if request.user.role == 'employee' and not request.user.is_superuser:
        employees_qs = employees_qs.filter(user=request.user)

    context = {
        'total_employees': employees_qs.count(),
        'total_departments': Department.objects.count(),
        'active_employees': employees_qs.filter(status='active').count(),
        'inactive_employees': employees_qs.filter(status='inactive').count(),
        'recent_employees': employees_qs.order_by('-created_at')[:5],
        'pending_leaves': Leave.objects.filter(status='pending').count(),
    }
    return render(request, 'dashboard/dashboard.html', context)

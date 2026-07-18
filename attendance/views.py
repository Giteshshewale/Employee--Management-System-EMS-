from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404

from accounts.decorators import admin_or_hr_required
from employees.models import Employee
from .models import Attendance
from .forms import AttendanceForm


@login_required
def attendance_list(request):
    records = Attendance.objects.select_related('employee').all()

    if request.user.role == 'employee' and not request.user.is_superuser:
        records = records.filter(employee__user=request.user)

    employee_id = request.GET.get('employee', '')
    if employee_id:
        records = records.filter(employee_id=employee_id)

    date = request.GET.get('date', '')
    if date:
        records = records.filter(date=date)

    paginator = Paginator(records, 15)
    page_obj = paginator.get_page(request.GET.get('page', 1))

    context = {
        'page_obj': page_obj,
        'employees': Employee.objects.all(),
        'selected_employee': employee_id,
        'selected_date': date,
    }
    return render(request, 'attendance/list.html', context)


@login_required
@admin_or_hr_required
def attendance_mark(request):
    if request.method == 'POST':
        form = AttendanceForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Attendance marked successfully.')
            except Exception:
                messages.error(request, 'Attendance for this employee on this date already exists.')
            return redirect('attendance:list')
    else:
        form = AttendanceForm()
    return render(request, 'attendance/form.html', {'form': form, 'title': 'Mark Attendance'})


@login_required
@admin_or_hr_required
def attendance_delete(request, pk):
    record = get_object_or_404(Attendance, pk=pk)
    if request.method == 'POST':
        record.delete()
        messages.success(request, 'Attendance record deleted.')
        return redirect('attendance:list')
    return render(request, 'attendance/confirm_delete.html', {'record': record})

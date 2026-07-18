from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from accounts.decorators import admin_or_hr_required
from .models import Department
from .forms import DepartmentForm


@login_required
def department_list(request):
    departments = Department.objects.all()
    return render(request, 'departments/list.html', {'departments': departments})


@login_required
@admin_or_hr_required
def department_add(request):
    if request.method == 'POST':
        form = DepartmentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Department added successfully.')
            return redirect('departments:list')
    else:
        form = DepartmentForm()
    return render(request, 'departments/form.html', {'form': form, 'title': 'Add Department'})


@login_required
@admin_or_hr_required
def department_update(request, pk):
    department = get_object_or_404(Department, pk=pk)
    if request.method == 'POST':
        form = DepartmentForm(request.POST, instance=department)
        if form.is_valid():
            form.save()
            messages.success(request, 'Department updated successfully.')
            return redirect('departments:list')
    else:
        form = DepartmentForm(instance=department)
    return render(request, 'departments/form.html', {'form': form, 'title': 'Update Department'})


@login_required
@admin_or_hr_required
def department_delete(request, pk):
    department = get_object_or_404(Department, pk=pk)
    if request.method == 'POST':
        department.delete()
        messages.success(request, 'Department deleted successfully.')
        return redirect('departments:list')
    return render(request, 'departments/confirm_delete.html', {'department': department})

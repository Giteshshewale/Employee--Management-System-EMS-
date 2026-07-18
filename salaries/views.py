from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, redirect

from accounts.decorators import admin_or_hr_required
from notifications.utils import create_notification
from .models import Salary
from .forms import SalaryForm


@login_required
def salary_list(request):
    records = Salary.objects.select_related('employee').all()

    if request.user.role == 'employee' and not request.user.is_superuser:
        records = records.filter(employee__user=request.user)

    paginator = Paginator(records, 15)
    page_obj = paginator.get_page(request.GET.get('page', 1))
    return render(request, 'salaries/list.html', {'page_obj': page_obj})


@login_required
@admin_or_hr_required
def salary_add(request):
    if request.method == 'POST':
        form = SalaryForm(request.POST)
        if form.is_valid():
            salary = form.save()
            create_notification(
                salary.employee.user if salary.employee.user else request.user,
                f'Salary for {salary.month} has been updated.'
            )
            messages.success(request, 'Salary record saved successfully.')
            return redirect('salaries:list')
    else:
        form = SalaryForm()
    return render(request, 'salaries/form.html', {'form': form, 'title': 'Add Salary Record'})

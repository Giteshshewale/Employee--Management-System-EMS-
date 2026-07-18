from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from accounts.decorators import admin_or_hr_required
from notifications.utils import create_notification
from .models import Leave
from .forms import LeaveApplyForm


@login_required
def leave_list(request):
    leaves = Leave.objects.select_related('employee').all()

    if request.user.role == 'employee' and not request.user.is_superuser:
        leaves = leaves.filter(employee__user=request.user)

    status = request.GET.get('status', '')
    if status:
        leaves = leaves.filter(status=status)

    paginator = Paginator(leaves, 15)
    page_obj = paginator.get_page(request.GET.get('page', 1))
    return render(request, 'leaves/list.html', {'page_obj': page_obj, 'selected_status': status})


@login_required
def leave_apply(request):
    employee_profile = getattr(request.user, 'employee_profile', None)
    if employee_profile is None:
        messages.error(request, 'Your account is not linked to an employee record yet. Contact HR.')
        return redirect('leaves:list')

    if request.method == 'POST':
        form = LeaveApplyForm(request.POST)
        if form.is_valid():
            leave = form.save(commit=False)
            leave.employee = employee_profile
            leave.save()
            messages.success(request, 'Leave application submitted.')
            return redirect('leaves:list')
    else:
        form = LeaveApplyForm()
    return render(request, 'leaves/form.html', {'form': form, 'title': 'Apply for Leave'})


@login_required
@admin_or_hr_required
def leave_review(request, pk, action):
    leave = get_object_or_404(Leave, pk=pk)
    if action not in ('approve', 'reject'):
        messages.error(request, 'Invalid action.')
        return redirect('leaves:list')

    leave.status = Leave.Status.APPROVED if action == 'approve' else Leave.Status.REJECTED
    leave.reviewed_on = timezone.now()
    leave.save()

    create_notification(
        leave.employee.user if leave.employee.user else request.user,
        f'Your leave request ({leave.from_date} to {leave.to_date}) was {leave.get_status_display().lower()}.'
    )
    send_mail(
        subject=f'Leave request {leave.get_status_display()}',
        message=f'Hi {leave.employee.full_name}, your leave request from {leave.from_date} to '
                f'{leave.to_date} has been {leave.get_status_display().lower()}.',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[leave.employee.email],
        fail_silently=True,
    )
    messages.success(request, f'Leave request {leave.get_status_display().lower()}.')
    return redirect('leaves:list')

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.core.paginator import Paginator

from .models import Notification


@login_required
def notification_list(request):
    notifications = Notification.objects.filter(user=request.user)
    paginator = Paginator(notifications, 20)
    page_obj = paginator.get_page(request.GET.get('page', 1))
    return render(request, 'notifications/list.html', {'page_obj': page_obj})


@login_required
def mark_all_read(request):
    Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
    return redirect('notifications:list')

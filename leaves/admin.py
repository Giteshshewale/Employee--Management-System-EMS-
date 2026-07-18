from django.contrib import admin
from .models import Leave


@admin.register(Leave)
class LeaveAdmin(admin.ModelAdmin):
    list_display = ['employee', 'from_date', 'to_date', 'status', 'applied_on']
    list_filter = ['status']
    search_fields = ['employee__first_name', 'employee__last_name']

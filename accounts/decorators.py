from functools import wraps
from django.contrib import messages
from django.shortcuts import redirect


def role_required(*allowed_roles):
    """
    Restrict a view to users whose `role` is in allowed_roles.
    Superusers / admin role always pass.
    Usage: @role_required('admin', 'hr')
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            user = request.user
            if not user.is_authenticated:
                return redirect('accounts:login')
            if user.is_superuser or user.role == 'admin' or user.role in allowed_roles:
                return view_func(request, *args, **kwargs)
            messages.error(request, "You don't have permission to access that page.")
            return redirect('dashboard:dashboard')
        return wrapper
    return decorator


def admin_or_hr_required(view_func):
    return role_required('admin', 'hr')(view_func)

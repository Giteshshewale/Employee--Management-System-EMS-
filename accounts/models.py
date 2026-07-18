from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """
    Custom user model with role-based access control (module 18):
    - admin: full access to everything
    - hr: manage employees, departments, attendance, leave
    - employee: can only view/edit their own profile
    """

    class Role(models.TextChoices):
        ADMIN = 'admin', 'Admin'
        HR = 'hr', 'HR'
        EMPLOYEE = 'employee', 'Employee'

    role = models.CharField(max_length=10, choices=Role.choices, default=Role.EMPLOYEE)
    phone = models.CharField(max_length=15, blank=True)

    @property
    def is_admin_role(self):
        return self.role == self.Role.ADMIN or self.is_superuser

    @property
    def is_hr_role(self):
        return self.role == self.Role.HR

    @property
    def is_employee_role(self):
        return self.role == self.Role.EMPLOYEE

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"

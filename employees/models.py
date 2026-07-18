from django.conf import settings
from django.db import models
from departments.models import Department


def profile_photo_path(instance, filename):
    return f'profile_photos/{instance.employee_id}_{filename}'


def resume_path(instance, filename):
    return f'resumes/{instance.employee_id}_{filename}'


class Employee(models.Model):
    class Gender(models.TextChoices):
        MALE = 'M', 'Male'
        FEMALE = 'F', 'Female'
        OTHER = 'O', 'Other'

    class Status(models.TextChoices):
        ACTIVE = 'active', 'Active'
        INACTIVE = 'inactive', 'Inactive'

    # Optional link to a login account (so an "employee" role user can view own profile)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='employee_profile'
    )

    employee_id = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    gender = models.CharField(max_length=1, choices=Gender.choices, default=Gender.OTHER)
    dob = models.DateField(verbose_name='Date of Birth')
    joining_date = models.DateField()
    salary = models.DecimalField(max_digits=10, decimal_places=2, help_text='Basic salary')
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, related_name='employees')
    designation = models.CharField(max_length=100)

    address = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)
    pin_code = models.CharField(max_length=10, blank=True)

    profile_photo = models.ImageField(upload_to=profile_photo_path, blank=True, null=True)
    resume = models.FileField(upload_to=resume_path, blank=True, null=True)

    status = models.CharField(max_length=10, choices=Status.choices, default=Status.ACTIVE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.employee_id} - {self.full_name}'

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    @property
    def is_active_employee(self):
        return self.status == self.Status.ACTIVE

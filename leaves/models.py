from django.db import models
from employees.models import Employee


class Leave(models.Model):
    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending'
        APPROVED = 'approved', 'Approved'
        REJECTED = 'rejected', 'Rejected'

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='leaves')
    from_date = models.DateField()
    to_date = models.DateField()
    reason = models.TextField()
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING)
    applied_on = models.DateTimeField(auto_now_add=True)
    reviewed_on = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-applied_on']

    def __str__(self):
        return f'{self.employee.full_name} - {self.from_date} to {self.to_date} ({self.get_status_display()})'

    @property
    def days_requested(self):
        return (self.to_date - self.from_date).days + 1

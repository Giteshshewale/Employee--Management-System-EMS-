from django.db import models
from employees.models import Employee


class Salary(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='salary_records')
    month = models.CharField(max_length=20, help_text="e.g. 'July 2026'")
    basic_salary = models.DecimalField(max_digits=10, decimal_places=2)
    hra = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    da = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    bonus = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ('employee', 'month')

    def __str__(self):
        return f'{self.employee.full_name} - {self.month}'

    @property
    def total_salary(self):
        return self.basic_salary + self.hra + self.da + self.bonus

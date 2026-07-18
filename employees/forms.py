from django import forms
from .models import Employee


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = [
            'employee_id', 'first_name', 'last_name', 'email', 'phone', 'gender',
            'dob', 'joining_date', 'salary', 'department', 'designation',
            'address', 'city', 'state', 'country', 'pin_code',
            'profile_photo', 'resume', 'status',
        ]
        widgets = {
            'dob': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'joining_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'address': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if name in ('profile_photo', 'resume'):
                field.widget.attrs.setdefault('class', 'form-control')
            elif isinstance(field.widget, (forms.Select,)):
                field.widget.attrs.setdefault('class', 'form-select')
            elif not field.widget.attrs.get('class'):
                field.widget.attrs.setdefault('class', 'form-control')

    def clean_resume(self):
        resume = self.cleaned_data.get('resume')
        if resume and hasattr(resume, 'name'):
            valid_extensions = ('.pdf', '.doc', '.docx')
            if not resume.name.lower().endswith(valid_extensions):
                raise forms.ValidationError('Resume must be a PDF, DOC, or DOCX file.')
        return resume

    def clean_profile_photo(self):
        photo = self.cleaned_data.get('profile_photo')
        if photo and hasattr(photo, 'name'):
            valid_extensions = ('.jpg', '.jpeg', '.png')
            if not photo.name.lower().endswith(valid_extensions):
                raise forms.ValidationError('Profile photo must be a JPG, JPEG, or PNG file.')
        return photo

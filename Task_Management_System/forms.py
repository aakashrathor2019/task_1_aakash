from django import forms
from .models import Task
from django.core.exceptions import ValidationError
from django.utils import timezone

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = [
            'title',
            'description',
            'assigned_to',
            'start_date',
            'end_date',
            'priority',
            'status',
        ]
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def clean_end_date(self):
        start_date = self.cleaned_data.get('start_date')
        end_date = self.cleaned_data.get('end_date')

        if not start_date or not end_date:
            raise ValidationError("Start date and end date are required.")

         
        if end_date < timezone.now():
            raise ValidationError("End date cannot be in the past.")

        if end_date.date() < start_date:
            raise ValidationError("End date must be after the start date.")

        return end_date

    def clean(self):
        cleaned_data = super().clean()
 
        assigned_to = cleaned_data.get('assigned_to')
        assigned_by = cleaned_data.get('assigned_by')

        if assigned_to and assigned_by and assigned_to == assigned_by:
            raise ValidationError("Assigned to and Assigned by cannot be the same user.")

        return cleaned_data
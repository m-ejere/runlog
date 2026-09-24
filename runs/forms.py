from django import forms
from django.utils import timezone

from .models import Run


class RunForm(forms.ModelForm):
    class Meta:
        model = Run
        fields = ['date', 'distance', 'duration', 'run_type', 'notes']
        widgets = {
            'date': forms.DateInput(
                attrs={
                    'type': 'date',
                    'max': timezone.localdate().isoformat(),
                    'min': '1900-01-01',
                }
            ),
            'duration': forms.TimeInput(
                attrs={
                    'type': 'time',
                }
            ),
            'distance': forms.NumberInput(
                attrs={
                    'min': '0.01',
                    'step': '0.01',
                }
            ),
        }

    def clean_date(self):
        date = self.cleaned_data['date']
        minimum_date = timezone.datetime(1900, 1, 1).date()
        today = timezone.localdate()

        if date < minimum_date:
            raise forms.ValidationError(
                'Please enter a valid run date.'
            )

        if date > today:
            raise forms.ValidationError(
                'You cannot add a run in the future.'
            )

        return date

    def clean_distance(self):
        distance = self.cleaned_data['distance']

        if distance <= 0:
            raise forms.ValidationError(
                'Distance must be greater than 0.'
            )

        return distance

    def clean_duration(self):
        duration = self.cleaned_data['duration']

        if duration.total_seconds() <= 0:
            raise forms.ValidationError(
                'Duration must be greater than 0.'
            )

        return duration
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
                }
            ),
            'duration': forms.TimeInput(
                attrs={'type': 'time'}
            ),
        }

    def clean_date(self):
        date = self.cleaned_data['date']

        if date > timezone.localdate():
            raise forms.ValidationError(
                'You cannot add a run in the future.'
            )

        return date
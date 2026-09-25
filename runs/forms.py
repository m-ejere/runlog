from datetime import timedelta

from django import forms
from django.utils import timezone

from .models import Run


class RunForm(forms.ModelForm):
    hours = forms.IntegerField(
        min_value=0,
        max_value=23,
        initial=0,
        widget=forms.NumberInput(
            attrs={
                'min': '0',
                'max': '23',
                'placeholder': 'Hours',
            }
        ),
    )

    minutes = forms.IntegerField(
        min_value=0,
        max_value=59,
        initial=0,
        widget=forms.NumberInput(
            attrs={
                'min': '0',
                'max': '59',
                'placeholder': 'Minutes',
            }
        ),
    )

    seconds = forms.IntegerField(
        min_value=0,
        max_value=59,
        initial=0,
        widget=forms.NumberInput(
            attrs={
                'min': '0',
                'max': '59',
                'placeholder': 'Seconds',
            }
        ),
    )

    class Meta:
        model = Run
        fields = [
            'date',
            'distance',
            'distance_unit',
            'run_type',
            'notes',
        ]
        widgets = {
            'date': forms.DateInput(
                attrs={
                    'type': 'date',
                    'max': timezone.localdate().isoformat(),
                    'min': '1900-01-01',
                }
            ),
            'distance': forms.NumberInput(
                attrs={
                    'min': '0.01',
                    'step': '0.01',
                    'placeholder': 'e.g. 5.00',
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance and self.instance.pk:
            total_seconds = int(
                self.instance.duration.total_seconds()
            )

            self.fields['hours'].initial = total_seconds // 3600
            self.fields['minutes'].initial = (
                total_seconds % 3600
            ) // 60
            self.fields['seconds'].initial = total_seconds % 60

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

    def clean(self):
        cleaned_data = super().clean()

        hours = cleaned_data.get('hours')
        minutes = cleaned_data.get('minutes')
        seconds = cleaned_data.get('seconds')

        if hours is None or minutes is None or seconds is None:
            return cleaned_data

        total_seconds = (
            hours * 3600
            + minutes * 60
            + seconds
        )

        if total_seconds <= 0:
            raise forms.ValidationError(
                'Duration must be greater than 0.'
            )

        duration = timedelta(seconds=total_seconds)

        cleaned_data['duration'] = duration

        self.instance.duration = duration

        return cleaned_data

    def save(self, commit=True):
        run = super().save(commit=False)

        run.duration = self.cleaned_data['duration']

        if commit:
            run.save()

        return run
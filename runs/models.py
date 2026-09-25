from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Run(models.Model):
    RUN_TYPES = [
        ('Easy', 'Easy Run'),
        ('Long', 'Long Run'),
        ('Tempo', 'Tempo Run'),
        ('Intervals', 'Intervals'),
        ('Race', 'Race'),
    ]

    DISTANCE_UNITS = [
        ('km', 'Kilometres (km)'),
        ('mi', 'Miles (mi)'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    distance = models.DecimalField(max_digits=6, decimal_places=2)
    distance_unit = models.CharField(
        max_length=2,
        choices=DISTANCE_UNITS,
        default='km'
    )
    duration = models.DurationField()
    run_type = models.CharField(max_length=20, choices=RUN_TYPES)
    notes = models.TextField(blank=True)

    def clean(self):
        minimum_date = timezone.datetime(1900, 1, 1).date()

        if self.date < minimum_date:
            raise ValidationError(
                {'date': 'Please enter a valid run date.'}
            )

        if self.date > timezone.localdate():
            raise ValidationError(
                {'date': 'You cannot add a run in the future.'}
            )

        if self.distance <= 0:
            raise ValidationError(
                {'distance': 'Distance must be greater than 0.'}
            )

        if (
            self.duration is not None
            and self.duration.total_seconds() <= 0
        ):
            raise ValidationError(
                {'duration': 'Duration must be greater than 0.'}
            )

    def __str__(self):
        return f"{self.user.username} - {self.date}"
from django.db import models
from django.contrib.auth.models import User


class Run(models.Model):
    RUN_TYPES = [
        ('Easy', 'Easy Run'),
        ('Long', 'Long Run'),
        ('Tempo', 'Tempo Run'),
        ('Intervals', 'Intervals'),
        ('Race', 'Race'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    distance = models.DecimalField(max_digits=6, decimal_places=2)
    duration = models.DurationField()
    run_type = models.CharField(max_length=20, choices=RUN_TYPES)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.date}"
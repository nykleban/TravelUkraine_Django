from django.db import models


class Place(models.Model):
    SEASON_CHOICES = [
        ('any', 'Будь-який сезон'),
        ('spring', 'Весна'),
        ('summer', 'Літо'),
        ('autumn', 'Осінь'),
        ('winter', 'Зима'),
    ]

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    region = models.CharField(max_length=100, blank=True)
    image = models.ImageField(upload_to='place_images/', null=True, blank=True)
    ideal_days_for_rest = models.PositiveIntegerField(default=1)
    
    best_season = models.CharField(max_length=20, choices=SEASON_CHOICES, default='any')

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

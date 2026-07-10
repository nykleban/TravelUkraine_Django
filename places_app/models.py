from django.core.files.storage import default_storage
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
    gallery_images = models.JSONField(default=list, blank=True)
    ideal_days_for_rest = models.PositiveIntegerField(default=1)
    
    best_season = models.CharField(max_length=20, choices=SEASON_CHOICES, default='any')

    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def preview_image_url(self):
        if self.gallery_images:
            return default_storage.url(self.gallery_images[0])

        return '/media/no_image_dir/no_image_place.png'

    @property
    def gallery_image_urls(self):
        return [
            default_storage.url(image_path)
            for image_path in self.gallery_images
            if image_path
        ]

    def __str__(self):
        return self.name

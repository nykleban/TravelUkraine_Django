from django import forms
from places_app.models import Place


class PlaceForm(forms.ModelForm):
    class Meta:
        model = Place
        fields = ['name', 'image_url', 'region', 'description', 'ideal_days_for_rest']
        labels = {
            'name': 'Назва',
            'image_url': 'Посилання на зображення',
            'region': 'Область',
            'description': 'Опис',
            'ideal_days_for_rest': 'Ідеальна кількість днів для відпочинку',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'image_url': forms.URLInput(attrs={'class': 'form-control'}),
            'region': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'ideal_days_for_rest': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 30}),
        }

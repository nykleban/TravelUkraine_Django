from django import forms
from places_app.models import Place


class PlaceForm(forms.ModelForm):
    class Meta:
        model = Place
        fields = ['name', 'region', 'description', 'ideal_days_for_rest', 'best_season']
        labels = {
            'name': 'Назва',
            'region': 'Область',
            'description': 'Опис',
            'ideal_days_for_rest': 'Ідеальна кількість днів для відпочинку',
            'best_season': 'Найкращий сезон',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'region': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'ideal_days_for_rest': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 30}),
            'best_season': forms.Select(attrs={'class': 'form-select'}),
        }

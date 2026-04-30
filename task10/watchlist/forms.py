from django import forms

from .models import Movie


class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ['title', 'genre', 'year', 'status', 'rating']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'genre': forms.TextInput(attrs={'class': 'form-control'}),
            'year': forms.NumberInput(attrs={'class': 'form-control', 'min': 1888}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'rating': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'max': 10,
            }),
        }

    def clean_rating(self):
        rating = self.cleaned_data['rating']
        if not 1 <= rating <= 10:
            raise forms.ValidationError('Rating must be between 1 and 10.')
        return rating

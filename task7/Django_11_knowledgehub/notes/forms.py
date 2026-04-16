from django import forms
from django.core.exceptions import ValidationError


class NoteForm(forms.Form):
    CATEGORY_CHOICES = [
        ("study", "Study"),
        ("work", "Work"),
        ("personal", "Personal"),
    ]

    title = forms.CharField(
        label="Title",
        max_length=150,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    content = forms.CharField(
        label="Content",
        widget=forms.Textarea(attrs={"class": "form-control", "rows": 5}),
    )
    category = forms.ChoiceField(
        label="Category",
        choices=CATEGORY_CHOICES,
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    tags = forms.CharField(
        label="Tags",
        help_text="Separate tags with commas.",
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "django, python, notes"}
        ),
    )

    def clean_title(self):
        title = self.cleaned_data["title"].strip()
        if title.lower().startswith("test"):
            raise ValidationError('Title must not start with the word "test".')
        return title

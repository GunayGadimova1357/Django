from django import forms

from .models import Article, Category


class ArticleForm(forms.ModelForm):
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        empty_label="Select a category",
    )

    class Meta:
        model = Article
        fields = ["title", "author", "category", "image", "excerpt", "content"]
        widgets = {
            "title": forms.TextInput(attrs={"placeholder": "Article title"}),
            "author": forms.TextInput(attrs={"placeholder": "Author name"}),
            "excerpt": forms.Textarea(attrs={"rows": 4}),
            "content": forms.Textarea(attrs={"rows": 10}),
        }

    def clean(self):
        cleaned_data = super().clean()
        image = cleaned_data.get("image")

        if not image:
            raise forms.ValidationError("Upload an image.")

        return cleaned_data

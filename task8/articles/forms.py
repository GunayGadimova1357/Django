from django import forms

from .models import Article, Category


class ArticleForm(forms.ModelForm):
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        empty_label="Select a category",
    )

    class Meta:
        model = Article
        fields = ["title", "category", "image", "content"]
        widgets = {
            "title": forms.TextInput(attrs={"placeholder": "Article title"}),
            "content": forms.Textarea(attrs={"rows": 10}),
        }

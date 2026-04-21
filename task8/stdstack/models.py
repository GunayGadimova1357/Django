from django.db import models
from django.urls import reverse

from .storage import CloudinaryFallbackStorage


class Category(models.Model):
    name = models.CharField(max_length=120, unique=True, verbose_name="Name")
    slug = models.SlugField(max_length=140, unique=True, verbose_name="Slug")

    class Meta:
        ordering = ["name"]
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Article(models.Model):
    title = models.CharField(max_length=200, verbose_name="Title")
    author = models.CharField(max_length=120, verbose_name="Author")
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="articles",
        verbose_name="Category",
    )

    image = models.FileField(
        upload_to="articles/",
        storage=CloudinaryFallbackStorage(),
        blank=True,
        verbose_name="Image",
        help_text="Uploads try Cloudinary first. If it rejects the file, the image is stored locally.",
    )

    excerpt = models.TextField(
        blank=True,
        verbose_name="Excerpt",
        help_text="If left empty, the preview will be generated from the article text.",
    )
    content = models.TextField(verbose_name="Full article")
    likes = models.PositiveIntegerField(default=0, verbose_name="Likes")
    dislikes = models.PositiveIntegerField(default=0, verbose_name="Dislikes")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Article"
        verbose_name_plural = "Articles"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("stdstack:article-detail", args=[self.pk])

    @property
    def preview_text(self):
        return self.excerpt or self.content[:220]

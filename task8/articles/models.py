from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Avg
from django.urls import reverse

from stdstack.storage import CloudinaryFallbackStorage

User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=120, unique=True, verbose_name="Name")
    slug = models.SlugField(max_length=140, unique=True, verbose_name="Slug")

    class Meta:
        app_label = "stdstack"
        ordering = ["name"]
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Article(models.Model):
    STATUS_PENDING = "pending"
    STATUS_APPROVED = "approved"
    STATUS_REJECTED = "rejected"
    STATUS_CHOICES = [
        (STATUS_PENDING, "Pending review"),
        (STATUS_APPROVED, "Approved"),
        (STATUS_REJECTED, "Rejected"),
    ]

    title = models.CharField(max_length=200, verbose_name="Title")
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="articles",
        verbose_name="Author",
    )
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
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_PENDING,
        db_index=True,
        verbose_name="Publication status",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = "stdstack"
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

    @property
    def rating(self):
        value = self.ratings.aggregate(avg=Avg("value"))["avg"]
        return round(value or 0, 1)

    @property
    def rating_count(self):
        return self.ratings.count()


class ArticleRating(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name="ratings")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="article_ratings")
    value = models.PositiveSmallIntegerField(choices=[(value, value) for value in range(1, 6)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = "stdstack"
        unique_together = ("article", "user")
        verbose_name = "Article rating"
        verbose_name_plural = "Article ratings"

    def __str__(self):
        return f"{self.user} rated {self.article} as {self.value}"


class Bookmark(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name="bookmarks")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bookmarks")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = "stdstack"
        unique_together = ("article", "user")
        ordering = ["-created_at"]
        verbose_name = "Bookmark"
        verbose_name_plural = "Bookmarks"

    def __str__(self):
        return f"{self.user} bookmarked {self.article}"

from django.contrib import admin

from .models import Article, ArticleRating, Bookmark, Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    search_fields = ("name", "slug")


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "category", "status", "rating", "created_at")
    list_filter = ("category", "status", "created_at")
    search_fields = ("title", "author__username", "content")
    actions = ("approve_articles", "reject_articles")

    @admin.action(description="Approve selected articles")
    def approve_articles(self, request, queryset):
        queryset.update(status=Article.STATUS_APPROVED)

    @admin.action(description="Reject selected articles")
    def reject_articles(self, request, queryset):
        queryset.update(status=Article.STATUS_REJECTED)


@admin.register(ArticleRating)
class ArticleRatingAdmin(admin.ModelAdmin):
    list_display = ("article", "user", "value", "updated_at")
    list_filter = ("value", "updated_at")
    search_fields = ("article__title", "user__username")


@admin.register(Bookmark)
class BookmarkAdmin(admin.ModelAdmin):
    list_display = ("article", "user", "created_at")
    search_fields = ("article__title", "user__username")

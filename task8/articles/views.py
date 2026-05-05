import os
import uuid

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.db.models import Avg, Count, Q
from django.http import HttpResponseForbidden, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from accounts.permissions import can_manage_article, is_editor, is_not_banned

from .forms import ArticleForm
from .models import Article, ArticleRating, Bookmark, Category

User = get_user_model()


class ArticleQuerysetMixin:
    def base_queryset(self):
        queryset = (
            Article.objects.select_related("category", "author", "author__profile")
            .annotate(avg_rating=Avg("ratings__value"), rating_total=Count("ratings"))
        )
        if not is_editor(self.request.user):
            if self.request.user.is_authenticated:
                queryset = queryset.filter(Q(status=Article.STATUS_APPROVED) | Q(author=self.request.user))
            else:
                queryset = queryset.filter(status=Article.STATUS_APPROVED)
        return queryset


class ArticleListView(ArticleQuerysetMixin, ListView):
    model = Article
    template_name = "articles/article_list.html"
    context_object_name = "articles"

    def get_queryset(self):
        return self.base_queryset().order_by("-created_at")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Latest Articles"
        context["page_subtitle"] = "All approved articles ordered by creation time."
        return context


class PopularArticleListView(ArticleQuerysetMixin, ListView):
    model = Article
    template_name = "articles/article_list.html"
    context_object_name = "articles"

    def get_queryset(self):
        return (
            self.base_queryset()
            .filter(status=Article.STATUS_APPROVED)
            .annotate(popular_rating=Avg("ratings__value"))
            .filter(popular_rating__gte=4)
            .order_by("-popular_rating", "-created_at")
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Popular"
        context["page_subtitle"] = "Articles with an average rating of 4 or higher."
        return context


class CategoryArticleListView(ArticleQuerysetMixin, ListView):
    model = Article
    template_name = "articles/article_list.html"
    context_object_name = "articles"

    def dispatch(self, request, *args, **kwargs):
        self.category = get_object_or_404(Category, slug=kwargs["slug"])
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return self.base_queryset().filter(category=self.category).order_by("-created_at")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = self.category.name
        context["page_subtitle"] = "Articles from this category."
        return context


class FavoriteArticleListView(LoginRequiredMixin, ArticleQuerysetMixin, ListView):
    model = Article
    template_name = "articles/article_list.html"
    context_object_name = "articles"

    def get_queryset(self):
        return (
            self.base_queryset()
            .filter(bookmarks__user=self.request.user, status=Article.STATUS_APPROVED)
            .order_by("-bookmarks__created_at")
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Favorites"
        context["page_subtitle"] = "Articles saved in your bookmarks."
        return context


class ArticleDetailView(ArticleQuerysetMixin, DetailView):
    model = Article
    template_name = "articles/article_detail.html"
    context_object_name = "article"

    def get_queryset(self):
        return self.base_queryset()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        article = self.object
        user = self.request.user
        context["user_rating"] = None
        context["is_bookmarked"] = False
        context["can_edit_article"] = can_manage_article(user, article)
        if user.is_authenticated:
            rating = ArticleRating.objects.filter(article=article, user=user).first()
            context["user_rating"] = rating.value if rating else None
            context["is_bookmarked"] = Bookmark.objects.filter(article=article, user=user).exists()
        return context


class ArticleCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Article
    form_class = ArticleForm
    template_name = "articles/article_form.html"

    def test_func(self):
        return is_not_banned(self.request.user)

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.status = Article.STATUS_APPROVED if is_editor(self.request.user) else Article.STATUS_PENDING
        messages.success(self.request, "Article saved. It will be visible after admin approval.")
        return super().form_valid(form)


class ArticleUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Article
    form_class = ArticleForm
    template_name = "articles/article_form.html"

    def get_queryset(self):
        return Article.objects.select_related("author", "category")

    def test_func(self):
        article = self.get_object()
        return is_not_banned(self.request.user) and can_manage_article(self.request.user, article)

    def form_valid(self, form):
        form.instance.status = Article.STATUS_APPROVED if is_editor(self.request.user) else Article.STATUS_PENDING
        messages.success(self.request, "Article updated. Changes require admin approval.")
        return super().form_valid(form)


class ArticleDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Article
    template_name = "articles/article_confirm_delete.html"

    def get_success_url(self):
        return reverse("stdstack:article-list")

    def test_func(self):
        return can_manage_article(self.request.user, self.get_object())


def authors(request):
    users = User.objects.select_related("profile").annotate(
        approved_articles_count=Count("articles", filter=Q(articles__status=Article.STATUS_APPROVED))
    ).filter(approved_articles_count__gt=0).order_by("username")
    return render(request, "articles/authors.html", {"authors": users})


def author_articles(request, pk):
    author = get_object_or_404(User, pk=pk)
    articles = (
        Article.objects.select_related("category", "author")
        .annotate(avg_rating=Avg("ratings__value"), rating_total=Count("ratings"))
        .filter(author=author, status=Article.STATUS_APPROVED)
        .order_by("-created_at")
    )
    return render(
        request,
        "articles/article_list.html",
        {
            "articles": articles,
            "page_title": author.get_username(),
            "page_subtitle": "Approved articles by this author.",
        },
    )


def rate_article(request, pk):
    if request.method != "POST":
        return redirect("stdstack:article-detail", pk=pk)
    if not is_not_banned(request.user):
        return HttpResponseForbidden("Only active registered users can rate articles.")

    article = get_object_or_404(Article, pk=pk, status=Article.STATUS_APPROVED)
    if article.author == request.user:
        return HttpResponseForbidden("You cannot rate your own article.")
    value = int(request.POST.get("rating", 0))
    if value in range(1, 6):
        ArticleRating.objects.update_or_create(
            article=article,
            user=request.user,
            defaults={"value": value},
        )
    return HttpResponseRedirect(request.POST.get("next") or article.get_absolute_url())


def toggle_bookmark(request, pk):
    if request.method != "POST":
        return redirect("stdstack:article-detail", pk=pk)
    if not is_not_banned(request.user):
        return HttpResponseForbidden("Only active registered users can bookmark articles.")

    article = get_object_or_404(Article, pk=pk, status=Article.STATUS_APPROVED)
    bookmark, created = Bookmark.objects.get_or_create(article=article, user=request.user)
    if not created:
        bookmark.delete()
    return HttpResponseRedirect(request.POST.get("next") or article.get_absolute_url())


@login_required
def upload_image(request):
    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed"}, status=405)
    image = request.FILES.get("image")
    if not image:
        return JsonResponse({"error": "No image provided"}, status=400)
    ext = os.path.splitext(image.name)[1].lower() or ".jpg"
    filename = f"content_images/{uuid.uuid4().hex}{ext}"
    path = default_storage.save(filename, ContentFile(image.read()))
    return JsonResponse({"url": default_storage.url(path)})


def moderate_article(request, pk, action):
    if request.method != "POST":
        return redirect("stdstack:article-detail", pk=pk)
    if not is_editor(request.user):
        return HttpResponseForbidden("Only admins can moderate articles.")

    article = get_object_or_404(Article, pk=pk)
    if action == "approve":
        article.status = Article.STATUS_APPROVED
    elif action == "reject":
        article.status = Article.STATUS_REJECTED
    article.save(update_fields=["status", "updated_at"])
    return HttpResponseRedirect(request.POST.get("next") or article.get_absolute_url())

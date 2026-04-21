from django.db.models import F
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import CreateView, DetailView, ListView

from .forms import ArticleForm
from .models import Article


class ArticleListView(ListView):
    model = Article
    template_name = "stdstack/article_list.html"
    context_object_name = "articles"

    def get_queryset(self):
        return Article.objects.select_related("category")


class ArticleDetailView(DetailView):
    model = Article
    template_name = "stdstack/article_detail.html"
    context_object_name = "article"

    def get_queryset(self):
        return Article.objects.select_related("category")


class ArticleCreateView(CreateView):
    model = Article
    form_class = ArticleForm
    template_name = "stdstack/article_form.html"


def react_to_article(request, pk, reaction):
    if request.method != "POST":
        return redirect("stdstack:article-detail", pk=pk)

    article = get_object_or_404(Article, pk=pk)
    if reaction == "like":
        Article.objects.filter(pk=article.pk).update(likes=F("likes") + 1)
    elif reaction == "dislike":
        Article.objects.filter(pk=article.pk).update(dislikes=F("dislikes") + 1)

    redirect_to = request.POST.get("next") or reverse("stdstack:article-detail", args=[pk])
    return HttpResponseRedirect(redirect_to)


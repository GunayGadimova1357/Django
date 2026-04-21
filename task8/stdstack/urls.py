from django.urls import path

from .views import ArticleCreateView, ArticleDetailView, ArticleListView, react_to_article

app_name = "stdstack"

urlpatterns = [
    path("", ArticleListView.as_view(), name="article-list"),
    path("articles/create/", ArticleCreateView.as_view(), name="article-create"),
    path("articles/<int:pk>/", ArticleDetailView.as_view(), name="article-detail"),
    path(
        "articles/<int:pk>/<str:reaction>/",
        react_to_article,
        name="article-react",
    ),
]

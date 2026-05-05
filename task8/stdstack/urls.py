from django.contrib.auth import views as auth_views
from django.urls import path

from accounts.forms import BannedUserAuthenticationForm
from accounts.views import delete_account, profile_settings, register, update_user_role, users_admin
from articles.views import (
    ArticleCreateView,
    ArticleDeleteView,
    ArticleDetailView,
    ArticleListView,
    ArticleUpdateView,
    CategoryArticleListView,
    FavoriteArticleListView,
    PopularArticleListView,
    author_articles,
    authors,
    moderate_article,
    rate_article,
    toggle_bookmark,
    upload_image,
)

app_name = "stdstack"

urlpatterns = [
    path("", ArticleListView.as_view(), name="article-list"),
    path("popular/", PopularArticleListView.as_view(), name="article-popular"),
    path("categories/<slug:slug>/", CategoryArticleListView.as_view(), name="category-detail"),
    path("authors/", authors, name="authors"),
    path("authors/<int:pk>/", author_articles, name="author-detail"),
    path("favorites/", FavoriteArticleListView.as_view(), name="favorites"),
    path("articles/create/", ArticleCreateView.as_view(), name="article-create"),
    path("articles/<int:pk>/", ArticleDetailView.as_view(), name="article-detail"),
    path("articles/<int:pk>/edit/", ArticleUpdateView.as_view(), name="article-edit"),
    path("articles/<int:pk>/delete/", ArticleDeleteView.as_view(), name="article-delete"),
    path("articles/<int:pk>/rate/", rate_article, name="article-rate"),
    path("articles/<int:pk>/bookmark/", toggle_bookmark, name="article-bookmark"),
    path("articles/<int:pk>/moderate/<str:action>/", moderate_article, name="article-moderate"),
    path("articles/upload-image/", upload_image, name="article-upload-image"),
    path("profile/", profile_settings, name="profile-settings"),
    path("profile/delete/", delete_account, name="delete-account"),
    path("register/", register, name="register"),
    path(
        "login/",
        auth_views.LoginView.as_view(
            template_name="accounts/login.html",
            authentication_form=BannedUserAuthenticationForm,
        ),
        name="login",
    ),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("users/", users_admin, name="users-admin"),
    path("users/<int:pk>/<str:action>/", update_user_role, name="user-action"),
]

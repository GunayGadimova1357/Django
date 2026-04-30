from django.urls import path

from . import views


urlpatterns = [
    path('', views.movie_list, name='movie_list'),
    path('movies/add/', views.add_movie, name='add_movie'),
    path('movies/<int:pk>/edit/', views.edit_movie, name='edit_movie'),
    path('movies/<int:pk>/delete/', views.delete_movie, name='delete_movie'),
]

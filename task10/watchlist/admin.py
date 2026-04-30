from django.contrib import admin

from .models import Movie


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'genre', 'year', 'status', 'rating', 'user', 'created_at')
    list_filter = ('status', 'genre', 'year')
    search_fields = ('title', 'genre', 'user__username')

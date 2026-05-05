from django.contrib import admin

from .models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "is_banned")
    list_filter = ("is_banned",)
    search_fields = ("user__username",)

from django.contrib.auth import get_user_model
from django.db import models

from stdstack.storage import CloudinaryFallbackStorage

User = get_user_model()


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    is_banned = models.BooleanField(default=False)
    avatar = models.FileField(
        upload_to="avatars/",
        storage=CloudinaryFallbackStorage(),
        blank=True,
        verbose_name="Avatar",
    )

    class Meta:
        app_label = "stdstack"
        verbose_name = "User profile"
        verbose_name_plural = "User profiles"

    def __str__(self):
        return self.user.get_username()

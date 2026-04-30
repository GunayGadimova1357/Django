from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator


class Movie(models.Model):
    WANT_TO_WATCH = 'want'
    WATCHING = 'watching'
    WATCHED = 'watched'

    STATUS_CHOICES = [
        (WANT_TO_WATCH, 'Want to watch'),
        (WATCHING, 'Watching'),
        (WATCHED, 'Watched'),
    ]

    title = models.CharField('Movie title', max_length=255)
    genre = models.CharField('Genre', max_length=100)
    year = models.PositiveIntegerField('Release year')
    status = models.CharField(
        'Status',
        max_length=20,
        choices=STATUS_CHOICES,
        default=WANT_TO_WATCH,
    )
    rating = models.PositiveSmallIntegerField(
        'Personal rating',
        validators=[MinValueValidator(1), MaxValueValidator(10)],
    )
    created_at = models.DateTimeField('Date added', auto_now_add=True)
    user = models.ForeignKey(
        User,
        verbose_name='Owner',
        on_delete=models.CASCADE,
        related_name='movies',
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Movie'
        verbose_name_plural = 'Movies'

    def __str__(self):
        return self.title

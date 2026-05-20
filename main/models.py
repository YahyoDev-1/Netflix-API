from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Actor(models.Model):
    class GenderChoices(models.TextChoices):
        MALE = "M", "Male"
        FEMALE = "F", "Female"
        OTHER = "O", "Other"

    name = models.CharField(max_length=100, db_index=True)
    country = models.CharField(max_length=100, db_index=True)
    gender = models.CharField(max_length=1, choices=GenderChoices.choices)
    birth_date = models.DateField()

    class Meta:
        ordering = ["name"]
        indexes = [
            models.Index(fields=["country", "name"]),
        ]

    def __str__(self):
        return self.name


class Movie(models.Model):
    title = models.CharField(max_length=150, db_index=True)
    genre = models.CharField(max_length=50, db_index=True)
    release_year = models.PositiveSmallIntegerField(blank=True, null=True)
    actors = models.ManyToManyField(
        Actor,
        related_name="movies",
        blank=True
    )

    class Meta:
        ordering = ["-release_year", "title"]
        indexes = [
            models.Index(fields=["title"]),
            models.Index(fields=["genre"]),
        ]

    def __str__(self):
        return self.title


class Subscription(models.Model):
    title = models.CharField(max_length=100, unique=True)
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    duration = models.DurationField(help_text="For example: 30 days, 1 year")

    class Meta:
        ordering = ["price"]

    def __str__(self):
        return self.title


class Review(models.Model):
    movie = models.ForeignKey(
        Movie,
        on_delete=models.CASCADE,
        related_name="reviews"
    )
    comment = models.TextField()
    rate = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(5)]
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        short_comment = self.comment[:30]
        return f"{self.movie.title} - {self.rate}/5 - {short_comment}"

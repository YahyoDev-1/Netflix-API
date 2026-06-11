from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class Actor(models.Model):
    class GenderChoices(models.TextChoices):
        MALE = "M", "Male"
        FEMALE = "F", "Female"
        OTHER = "O", "Other"

    name = models.CharField(_('Name'), max_length=100, db_index=True)
    country = models.CharField(_('Country'), max_length=100, db_index=True)
    gender = models.CharField(_('Gender'), max_length=1, choices=GenderChoices.choices)
    birth_date = models.DateField(_('Birth Date'))

    class Meta:
        ordering = ["name"]
        indexes = [
            models.Index(fields=["country", "name"]),
        ]
        verbose_name = _("Actor")
        verbose_name_plural = _("Actors")

    def __str__(self):
        return self.name


class Movie(models.Model):
    title = models.CharField(_('Title'), max_length=150, db_index=True)
    genre = models.CharField(_('Genre'), max_length=50, db_index=True)
    release_year = models.PositiveSmallIntegerField(_('Release year'), blank=True, null=True)
    actors = models.ManyToManyField(
        Actor,
        related_name="movies",
        blank=True,
    )

    class Meta:
        ordering = ["-release_year", "title"]
        indexes = [
            models.Index(fields=["title"]),
            models.Index(fields=["genre"]),
        ]
        verbose_name = _("Movie")
        verbose_name_plural = _("Movies")

    def __str__(self):
        return self.title


class Subscription(models.Model):
    title = models.CharField(_('Title'), max_length=100, unique=True)
    price = models.DecimalField(
        _('Price'),
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    duration = models.DurationField(_('Duration'), help_text="For example: 30 days, 1 year")

    class Meta:
        ordering = ["price"]
        verbose_name = _("Subscription")
        verbose_name_plural = _("Subscriptions")

    def __str__(self):
        return self.title


class Review(models.Model):
    movie = models.ForeignKey(
        Movie,
        on_delete=models.CASCADE,
        related_name="reviews",
        verbose_name=_("Movie"),
    )
    comment = models.TextField(_('Comment'))
    rate = models.PositiveSmallIntegerField(_('Rate'),
                                            validators=[MinValueValidator(0), MaxValueValidator(5)]
                                            )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(_('Created at'), auto_now_add=True, db_index=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = _("Review")
        verbose_name_plural = _("Reviews")

    def __str__(self):
        short_comment = self.comment[:30]
        return f"{self.movie.title} - {self.rate}/5 - {short_comment}"

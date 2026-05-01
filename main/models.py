from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

# Create your models here.

class Actor(models.Model):
    gender_choice = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    gender = models.CharField(max_length=6, choices=gender_choice)
    birth_date = models.DateField()

    def __str__(self):
        return self.name

class Movie(models.Model):
    title = models.CharField(max_length=100)
    genre = models.CharField(max_length=100)
    year = models.IntegerField(blank=True, null=True)
    actors = models.ManyToManyField(Actor)

    def __str__(self):
        return self.title

class Subscription(models.Model):
    title = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration = models.DurationField()

    def __str__(self):
        return self.title

class Review(models.Model):
    comment = models.TextField()
    rate = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)])
    movie = models.ForeignKey(Movie, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.comment

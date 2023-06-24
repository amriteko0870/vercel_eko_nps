from django.db import models

# Create your models here.

class review_url(models.Model):
    user_id = models.CharField(max_length=50)
    url = models.TextField()
    feature_id = models.TextField()

class google_reviews(models.Model):
    user_id = models.CharField(max_length=50)
    name = models.CharField(max_length=200)
    review = models.TextField()
    rating = models.IntegerField()
    date = models.DateTimeField()
    sentiment = models.CharField(max_length=50)
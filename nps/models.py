from django.db import models
from datetime import datetime
import pytz

# Create your models here.

class nps_data(models.Model):
    user_id = models.CharField(max_length=50)
    review = models.TextField()
    nps = models.IntegerField()
    date = models.DateTimeField()
    sentiment = models.CharField(max_length=50)
    uploading_status = models.BooleanField(default=False)

class file_uploading_status(models.Model):
    user_id = models.CharField(max_length=50)
    status = models.CharField(max_length=150)

class upload_log(models.Model):
    user_id = models.CharField(max_length=50)
    file_name = models.CharField(max_length=200)
    date_time = models.DateTimeField(default=str(datetime.now(pytz.timezone("Asia/Kolkata"))))
    file_size = models.CharField(max_length=20)

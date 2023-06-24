from django.db import models

# Create your models here.

class user_data(models.Model):
    username = models.CharField(max_length=100,blank=False,null=False)
    email = models.CharField(max_length=100,blank=False,null=False)
    org_name = models.TextField(blank=False,null=False)
    password = models.CharField(max_length=100,blank=False,null=False)
    token = models.TextField(null=False,blank=False)

from django.urls import path
from user_auth.views import *

urlpatterns = [
                # path('index',index),
                path('create_user',create_user),
                path('login',login),
]
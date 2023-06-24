from django.urls import path
from google_reviews.views import *

urlpatterns = [
    path('add_url',add_url),
    path('get_rating',get_rating),
    path('netSentimentCard',netSentimentCard),
    path('net_cards',net_cards),
    path('all_comments',all_comments),
    path('all_alerts',all_alerts),
    path('nss_over_time',nss_over_time),
    path('rating_over_time',rating_over_time),
    path('rating_sentiment_over_time',rating_sentiment_over_time),

    # path('store_data',store_data),
]
from django.urls import path
from nps.views import *

urlpatterns = [
    path('nps_upload_button_status',nps_upload_button_status),
    path('file_upload',file_upload),
    path('net_promoter_score',net_promoter_score),
    path('netSentimentCard',netSentimentCard),
    path('net_cards',net_cards),
    path('all_comments',all_comments),
    path('all_alerts',all_alerts),
    path('nss_over_time',nss_over_time),
    path('nps_over_time',nps_over_time),
    path('nps_vs_sentiment',nps_vs_sentiment),
    path('upload_file_log',upload_file_log),


    path('test_api',test_api),
    path('delete_records',delete_records),
]

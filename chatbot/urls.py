# chatbot/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('reply_to_sms/', views.reply_to_sms, name='reply_to_sms'),
    path('view_notifications/', views.view_notifications, name='view_notifications'),
    # Define other URL patterns for different views
]

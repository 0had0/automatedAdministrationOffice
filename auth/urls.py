from django.urls import path

from .views import (LoginAPIView, register, authenticate_account)

app_name = 'auth'
urlpatterns = [
    path('register/', register),
    path('login/', LoginAPIView.as_view()),
    path('', authenticate_account)
]
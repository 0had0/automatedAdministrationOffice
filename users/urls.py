from django.urls import path

from .views import (DirectorAPIView, DirectorUserInteractionAPIView)

app_name = 'users'
urlpatterns = [
    path('directors/', DirectorAPIView.as_view()),
    path('users/', DirectorUserInteractionAPIView.as_view())
]
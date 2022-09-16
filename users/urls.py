from django.urls import path

from .views import (DirectorAPIView, DirectorUserInteractionAPIView, UsersAPIView)

app_name = 'users'
urlpatterns = [
    path('directors/', DirectorAPIView.as_view()),
    path('<int:user_id>/', UsersAPIView.as_view()),
    path('', DirectorUserInteractionAPIView.as_view()),
]
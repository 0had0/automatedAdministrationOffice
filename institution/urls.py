from django.urls import path

from .views import (InstitutionAPIView, get_institution, get_institution_users)

app_name = 'institution'
urlpatterns = [
    path('<int:institution_id>/', get_institution),
    path('<int:institution_id>/users', get_institution_users),
    path('', InstitutionAPIView.as_view())
]
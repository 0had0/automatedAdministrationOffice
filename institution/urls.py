from django.urls import path

from .views import (InstitutionAPIView, get_institution, get_institution_users, create_institution)

app_name = 'institution'
urlpatterns = [
    path('<int:institution_id>/', get_institution),
    path('<int:institution_id>/accounts', get_institution_users),
    path('create/', create_institution),
    path('', InstitutionAPIView.as_view())
]
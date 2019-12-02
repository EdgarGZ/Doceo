# Django
from django.urls import path

# Vistas
import apps.tutor.views as views


app_name='tutor'
urlpatterns = [
    path(
        route='<username>/',
        view=views.TutorDetailView.as_view(),
        name='tutor'
    ),
]
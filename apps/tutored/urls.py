# Django
from django.urls import path

# Views
import apps.tutored.views as views 


app_name='tutored'
urlpatterns = [
    path(
        route='<username>/',
        view=views.TutoredDetailView.as_view(),
        name='tutored'
    ),
    path(
        route='<username>/edit/',
        view=views.TutoredEditView.as_view(),
        name='edit'
    ),
    path(
        route='<username>/edit/user/',
        view=views.SaveEditProfileView.as_view(),
        name='save_edit_user'
    ),
    path(
        route='<username>/edit/password/',
        view=views.ChangePasswordView.as_view(),
        name='save_edit_password'
    ),
    path(
        route='<username>/edit/picture/',
        view=views.ChangeProfilePicView.as_view(),
        name='save_profile_pic'
    ),
    path(
        route='<username>/tutorias/',
        view=views.TutoriasTutoradoView.as_view(),
        name='tutorias'
    ),
]
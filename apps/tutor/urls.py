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
    path(
        route='<username>/add/subarea/',
        view=views.AddSubAreasView.as_view(),
        name='add_subarea'
    ),
    path(
        route='<username>/edit/',
        view=views.TutorEditView.as_view(),
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
        view=views.TutoriasTutorView.as_view(),
        name='tutorias'
    ),
    path(
        route='<username>/tutorias/add/schedule/',
        view=views.OfertarHorariosTutorView.as_view(),
        name='schedule'
    ),
    path(
        route='<username>/tutorias/get/last/notification/',
        view=views.LastNotificationReceived.as_view(),
        name='last_notification'
    ),
    path(
        route='<username>/tutorias/get/tutorship/notification/<id>/',
        view=views.TutoshipJsonResponse.as_view(),
        name='tutorship_json'
    ),
    path(
        route='<username>/tutorias/accept/tutorship/<tutoria>/<notificacion>/',
        view=views.AcceptTutoshipJsonResponse.as_view(),
        name='accept_tutorship_json'
    ),
]
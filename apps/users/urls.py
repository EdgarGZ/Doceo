# Django
from django.urls import path

# Views
import apps.users.views as views


app_name='users'
urlpatterns = [
    path(
        route='',
        view=views.LandingPageView.as_view(), 
        name='landing'
    ),

    path(
        route='sign_up/',
        view=views.SignUpOptionsView.as_view(), 
        name='sign_up_options'
    ),

    path(
        route='log_in/',
        view=views.LoginView.as_view(), 
        name='login_view'
    ),

    path(
        route='sign_up_tutorado/',
        view=views.SignUpTutoradoView.as_view(), 
        name='sign_up_tutorado'
    ),

    path(
        route='sign_up_tutor/',
        view=views.SignUpTutorView.as_view(), 
        name='sign_up_tutor'
    ),

    path(
        route='password_reset/',
        view=views.ResetPasswordRequestView.as_view(),
        name='password_reset'
    ),

    path(
        route='logout/',
        view=views.LogoutView.as_view(),
        name='logout'
    ),
]
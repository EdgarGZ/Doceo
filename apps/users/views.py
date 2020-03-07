# Django
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import TemplateView, FormView
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy, reverse
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.template import loader 
from django.core.validators import validate_email 
from django.core.exceptions import ValidationError
from django.core.mail import send_mail 
from django.views.generic import * 
from django.contrib import messages 

# Forms
from apps.users.forms import SignupBaseUserForm, SignupUserForm, SignupTutoradoForm, SignupTutorForm, PasswordResetRequestForm, SetPasswordForm

# Models
from django.contrib.auth.models import User
from apps.users.models import Usuario

# Doceo Settings
from doceo.settings import DEFAULT_FROM_EMAIL


# Create your views here.
class LandingPageView(TemplateView):
    template_name = 'landingPage.html'


class SignUpOptionsView(TemplateView):
    template_name = 'registro.html'


class LoginView(auth_views.LoginView):
    template_name = 'login.html'

    def get_success_url(self):
        """ Return to user's profile """
        if self.request.user.is_authenticated:
            usuario = Usuario.objects.get(user=self.request.user)
            if usuario.is_tutorado:
                return reverse('tutored:tutored', kwargs={'username': self.request.user.username})
            elif usuario.is_tutor:
                return reverse('tutor:tutor', kwargs={'username': self.request.user.username})


class SignUpTutoradoView(FormView):
    template_name = 'registro-tutorado.html'
    success_url = reverse_lazy('users:login_view')
    form_class = SignupBaseUserForm
    extra_context = {
        'user_form': SignupUserForm,
        'tutorado_form': SignupTutoradoForm
    }

    def form_invalid(self, form, user_form, tutorado_form):
        """If the form is invalid, render the invalid form."""
        return self.render_to_response(self.get_context_data(form=form, user_form=user_form, tutorado_form=tutorado_form))

    def form_valid(self, form, user_form, tutorado_form): 
        """ Save form data """
        form.save()
        user = User.objects.get(username=form.cleaned_data['username'])
        usuario = user_form.save(commit=False)
        usuario.user = user
        usuario.is_tutorado = True
        usuario.save()
        tutorado = tutorado_form.save(commit=False)
        tutorado.usuario = usuario
        tutorado.save()
        return HttpResponseRedirect(self.get_success_url())

    def post(self, request, *args, **kwargs):
        """ Save tutorado user in D.B. """
        form = self.get_form()
        user_form = SignupUserForm(self.request.POST, self.request.FILES)
        tutorado_form = SignupTutoradoForm(self.request.POST)

        if form.is_valid() and user_form.is_valid() and tutorado_form.is_valid():
            return self.form_valid(form, user_form, tutorado_form)
        else:
            return self.form_invalid(form, user_form, tutorado_form)


class SignUpTutorView(FormView):
    template_name = 'registro-tutor.html'
    success_url = reverse_lazy('users:login_view')
    form_class = SignupBaseUserForm
    extra_context = {
        'user_form': SignupUserForm,
        'tutor_form': SignupTutorForm
    }

    def form_invalid(self, form, user_form, tutor_form):
        """If the form is invalid, render the invalid form."""
        return self.render_to_response(self.get_context_data(form=form, user_form=user_form, tutor_form=tutor_form))

    def form_valid(self, form, user_form, tutor_form): 
        """ Save form data """
        form.save()
        user = User.objects.get(username=form.cleaned_data['username'])
        usuario = user_form.save(commit=False)
        usuario.user = user
        usuario.is_tutor = True
        usuario.save()
        tutor = tutor_form.save(commit=False)
        tutor.usuario = usuario
        tutor.save()
        return HttpResponseRedirect(self.get_success_url())

    def post(self, request, *args, **kwargs):
        """ Save tutor user in D.B. """
        print(request.POST)
        form = self.get_form()
        user_form = SignupUserForm(self.request.POST, self.request.FILES)
        tutor_form = SignupTutorForm(self.request.POST)

        if form.is_valid() and user_form.is_valid() and tutor_form.is_valid():
            return self.form_valid(form, user_form, tutor_form)
        else:
            return self.form_invalid(form, user_form, tutor_form)


class ResetPasswordRequestView(FormView):
    template_name = "recuperarPass.html"
    success_url = '/password_reset/'
    form_class = PasswordResetRequestForm

    @staticmethod
    def validate_email_address(email):
        try:
            validate_email(email)
            return True
        except ValidationError:
            return False

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            data = form.cleaned_data["correo"]
            if self.validate_email_address(data) is True:
                associated_users = Usuario.objects.filter(Q(correo=data))
            if associated_users.exists():
                usuario = Usuario.objects.get(correo=data)
                user = User.objects.get(username=usuario.user.username)
                c = {
                    'email': usuario.correo,
                    'domain': request.META['HTTP_HOST'],
                    'site_name': 'Portal C.D.',
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                    'user': user,
                    'token': default_token_generator.make_token(user),
                    'protocol': 'http',
                }
                subject_template_name = 'registration/password_reset_subject.txt'
                email_template_name = 'reiniciarPassEmail.html'
                subject = loader.render_to_string(subject_template_name, c)
                subject = ''.join(subject.splitlines())
                email = loader.render_to_string(email_template_name, c)
                send_mail(subject, email, DEFAULT_FROM_EMAIL, [
                          usuario.correo], fail_silently=False)
                result = self.form_valid(form)
                messages.success(request, 'Se ha enviado un correo a ' +
                                 data + ". Por favor, checa tu bandeja de entrada.")
                return result
            result = self.form_invalid(form)
            messages.error(
                request, 'No hay usuarios con el correo proporcionado')
            return result


class PasswordResetConfirmView(FormView):
    template_name = "recuperarPass.html"
    success_url = "/"
    form_class = SetPasswordForm

    def post(self, request, uidb64=None, token=None, *arg, **kwargs):
        UserModel = User
        form = self.form_class(request.POST)
        assert uidb64 is not None and token is not None
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = UserModel._default_manager.get(pk=uid)
        except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            if form.is_valid():
                new_password = form.cleaned_data['new_password2']
                user.set_password(new_password)
                user.save()
                messages.success(
                    request, 'Se reestablecio la contraseña con exito!.')
                return self.form_valid(form)
            else:
                messages.error(
                    request, 'La contraseña no se puedo reestablecer.')
                return self.form_invalid(form)
        else:
            messages.error(request, 'Este enlace ya no es valido!.')
            return self.form_invalid(form)


class LogoutView(LoginRequiredMixin, auth_views.LogoutView):
    """ Logout view """
    template_name = ''
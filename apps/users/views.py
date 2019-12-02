# Django
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import TemplateView, FormView
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy, reverse
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin

# Forms
from apps.users.forms import SignupBaseUserForm, SignupUserForm, SignupTutoradoForm, SignupTutorForm

# Models
from django.contrib.auth.models import User
from apps.users.models import Usuario


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


class LogoutView(LoginRequiredMixin, auth_views.LogoutView):
    """ Logout view """
    template_name = ''
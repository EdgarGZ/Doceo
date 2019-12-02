# Djangi
from django.shortcuts import render, reverse
from django.views.generic import DetailView, FormView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.contrib.auth import update_session_auth_hash

# Models
from django.contrib.auth.models import User
from apps.users.models import Usuario
from apps.tutor.models import Tutor


# Create your views here.
class TutorDetailView(LoginRequiredMixin, DetailView):
    """ Tutored detail view. """

    template_name = 'tutor/perfil-tutor-vistat.html'
    slug_field = 'username'
    slug_url_kwarg = 'username' # del lado del path de las urls
    queryset = User.objects.all()
    context_object_name = 'user'

    def get_context_data(self, **kwargs):
        """ Add user's extended models to context """
        context = super().get_context_data(**kwargs)
        user = self.get_object()
        context['usuario'] = Usuario.objects.get(user=user)
        context['tutor'] = Tutor.objects.get(usuario=context['usuario'])
        return context
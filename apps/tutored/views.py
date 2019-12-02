# Django
from django.shortcuts import render, reverse
from django.views.generic import DetailView, FormView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.contrib.auth import update_session_auth_hash

# Models
from django.contrib.auth.models import User
from apps.users.models import Usuario
from apps.tutored.models import Tutorado

# Forms
from apps.tutored.forms import EditProfileTutoredForm, ChangePasswordForm, ChangeProfilePicForm


# Create your views here.
class TutoredDetailView(LoginRequiredMixin, DetailView):
    """ Tutored detail view. """

    template_name = 'tutored/perfil-tutorado-vistat.html'
    slug_field = 'username'
    slug_url_kwarg = 'username' # del lado del path de las urls
    queryset = User.objects.all()
    context_object_name = 'user'

    def get_context_data(self, **kwargs):
        """ Add user's extended models to context """
        context = super().get_context_data(**kwargs)
        user = self.get_object()
        context['usuario'] = Usuario.objects.get(user=user)
        context['tutorado'] = Tutorado.objects.get(usuario=context['usuario'])
        return context


class TutoredEditView(LoginRequiredMixin, DetailView):
    """ Tutored edit view. """

    template_name = 'tutored/editar-perfil.html'
    slug_field = 'username'
    slug_url_kwarg = 'username' # del lado del path de las urls
    queryset = User.objects.all()
    context_object_name = 'user'

    def get_context_data(self, **kwargs):
        """ Add user's extended models to context """
        context = super().get_context_data(**kwargs)
        user = self.get_object()
        context['usuario'] = Usuario.objects.get(user=user)
        context['tutorado'] = Tutorado.objects.get(usuario=context['usuario'])
        return context


class SaveEditProfileView(LoginRequiredMixin, FormView):
    template_name = 'tutored/editar-perfil.html'
    form_class = EditProfileTutoredForm

    def get_context_data(self, **kwargs):
        """ Add user's extended models to context """
        context = super().get_context_data(**kwargs)
        user = User.objects.get(id=self.request.user.id)
        context['usuario'] = Usuario.objects.get(user=user)
        context['tutorado'] = Tutorado.objects.get(usuario=context['usuario'])
        return context

    def form_invalid(self, form):
        """If the form is invalid, render the invalid form."""
        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form): 
        """ Save form data """
        nombre = form.cleaned_data['nombre']
        correo = form.cleaned_data['correo']
        descripcion = form.cleaned_data['descripcion']
        usuario = Usuario.objects.get(user=self.request.user)
        usuario.nombre = nombre
        usuario.correo = correo
        usuario.descripcion = descripcion
        usuario.save()
        return HttpResponseRedirect(self.get_success_url())

    def post(self, request, *args, **kwargs):
        """ Save user new info in D.B. """
        user_form = EditProfileTutoredForm(self.request.POST)

        if user_form.is_valid():
            return self.form_valid(user_form)
        else:
            return self.form_invalid(user_form)

    def get_success_url(self):
        success_url = reverse('tutored:tutored', kwargs={'username': self.request.user.username})
        return str(success_url)


class ChangePasswordView(LoginRequiredMixin, FormView):
    template_name = 'tutored/editar-perfil.html'
    form_class = ChangePasswordForm

    def get_context_data(self, **kwargs):
        """ Add user's extended models to context """
        user = User.objects.get(id=self.request.user.id)
        kwargs['usuario'] = Usuario.objects.get(user=user)
        kwargs['tutorado'] = Tutorado.objects.get(usuario=kwargs['usuario'])
        return super().get_context_data(**kwargs)

    def form_invalid(self, form):
        """If the form is invalid, render the invalid form."""
        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form): 
        """ Save form data """
        password = form.cleaned_data['password']
        user = User.objects.get(id=self.request.user.id)
        user.set_password(password)
        user.save()
        update_session_auth_hash(request, user)
        return HttpResponseRedirect(self.get_success_url())

    def post(self, request, *args, **kwargs):
        """ Save user new info in D.B. """
        pass_form = ChangePasswordForm(self.request.POST, request=self.request)
        user = User.objects.get(id=self.request.user.id)
        if pass_form.is_valid():
            return self.form_valid(pass_form)
        else:
            return self.form_invalid(pass_form)

    def get_success_url(self):
        success_url = reverse('tutored:tutored', kwargs={'username': self.request.user.username})
        return str(success_url)
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs


class ChangeProfilePicView(LoginRequiredMixin, FormView):
    template_name = 'tutored/editar-perfil.html'
    form_class = ChangeProfilePicForm

    def get_context_data(self, **kwargs):
        """ Add user's extended models to context """
        user = User.objects.get(id=self.request.user.id)
        kwargs['usuario'] = Usuario.objects.get(user=user)
        kwargs['tutorado'] = Tutorado.objects.get(usuario=kwargs['usuario'])
        return super().get_context_data(**kwargs)

    def form_invalid(self, form):
        """If the form is invalid, render the invalid form."""
        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form): 
        """ Save form data """
        form.save()
        return HttpResponseRedirect(self.get_success_url())

    def post(self, request, *args, **kwargs):
        """ Save user new info in D.B. """
        usuario = Usuario.objects.get(user=self.request.user)
        form = ChangeProfilePicForm(self.request.POST, self.request.FILES, instance=usuario)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_success_url(self):
        success_url = reverse('tutored:tutored', kwargs={'username': self.request.user.username})
        return str(success_url)


class TutoriasTutoradoView(TemplateView):
    template_name = 'tutored/tutorias-tutorado.html'
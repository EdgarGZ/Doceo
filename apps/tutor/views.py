# Djangi
from django.shortcuts import render, reverse
from django.views.generic import DetailView, FormView, TemplateView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.contrib.auth import update_session_auth_hash

# Models
from django.contrib.auth.models import User
from apps.users.models import Usuario
from apps.tutor.models import Tutor
from apps.knowledge_area.models import SubAreasEspecialidad

# Forms
from apps.tutor.forms import EditProfileTutorForm, ChangePasswordForm, ChangeProfilePicForm, AddSubAreaForm

# Constants
SUBAREAS = (
    ('programación', [
        ('paradigmas', 'Paradigmas de Programación'),
        ('poo', 'Programación Orientada a Objetos'),
        ('back end', 'Back End'),
        ('patrones', 'Patrones de Diseño'),
    ]),
    ('matemáticas', [
        ('algebra', 'Algebra Lineal'),
        ('calculo', 'Calculo'),
        ('computacionales', 'Matematicas Computacionales'),
        ('estadistica', 'Probabilidad y Estadistica'),
    ]),
    ('redes', [
        ('diseño', 'Diseño de redes'),
        ('configuracion', 'Configuración de Redes'),
        ('administracion', 'Administración de Redes'),
    ]),
    ('front end', [
        ('ui', 'User Interfaces'),
        ('ux', 'User Experience'),
        ('maquetado', 'Maquetado de interfaces'),
    ]),
    ('ingles', [
        ('ingles uno', 'Ingles I'),
        ('ingles dos', 'Ingles II'),
        ('ingles tres', 'Ingles III'),
        ('ingles cuatro', 'Ingles IV'),
        ('preparación', 'Preparación TOEFL'),
    ]),
    ('bases de datos', [
        ('administracion', 'Administración de B.D.'),
        ('sql', 'SQL'),
        ('no sql', 'NoSQL'),
    ]),
    ('paralelo', [
        ('cuda', 'Cuda'),
        ('pycuda', 'PyCuda'),
    ]),
    ('imagenes', [
        ('movimiento', 'Detección de Movimiento'),
        ('objetos', 'Detección de Objetos'),
    ]),
)


# Create your views here.
class TutorDetailView(LoginRequiredMixin, DetailView):
    """ Tutored detail view. """

    template_name = 'tutor/perfil-tutor-vistat.html'
    slug_field = 'username'
    slug_url_kwarg = 'username' # del lado del path de las urls
    queryset = User.objects.all()
    context_object_name = 'user'
    extra_context = {
        'subarea_form': AddSubAreaForm
    }

    def get_context_data(self, **kwargs):
        """ Add user's extended models to context """
        context = super().get_context_data(**kwargs)
        user = self.get_object()
        context['usuario'] = Usuario.objects.get(user=user)
        context['tutor'] = Tutor.objects.get(usuario=context['usuario'])
        context['my_subareas'] = SubAreasEspecialidad.objects.filter(tutor = context['tutor'])
        context['subareas'] = {subarea[0]: subarea[1] for subarea in self.get_subareas(area_especialidad = context['tutor'].area_especialidad).pop()}
        context['mis_subareas'] = self.get_mis_subareas()
        context['subarea_form'] = AddSubAreaForm(request=self.request)
        return context

    def get_subareas(self, **kwargs):
        """ [UNUSED] Retrieves subareas based on favorite user's area """
        area_especialidad = kwargs['area_especialidad']

        return [subarea[1] for subarea in SUBAREAS if subarea[0] == area_especialidad]

    def get_mis_subareas(self):
        """ Retrieves user´s subareas stored in DB """
        subareas_guardadas = SubAreasEspecialidad.objects.filter(tutor=self.request.user.usuario.tutor)
        subareas_list = [subarea[1] for subarea in SUBAREAS if subarea[0] == self.request.user.usuario.tutor.area_especialidad]
        mis_subareas = [subareat for subareal in subareas_list for subareat in subareal for sag in subareas_guardadas if sag.subarea == subareat[0]]

        return mis_subareas


class AddSubAreasView(LoginRequiredMixin, FormView):
    template_name = 'tutor/perfil-tutor-vistat.html'
    form_class = AddSubAreaForm

    def get_context_data(self, **kwargs):
        """ Add user's extended models to context """
        context = super().get_context_data(**kwargs)
        user = User.objects.get(id=self.request.user.id)
        context['usuario'] = Usuario.objects.get(user=user)
        context['tutor'] = Tutor.objects.get(usuario=context['usuario'])
        return context

    def form_invalid(self, form):
        """If the form is invalid, render the invalid form."""
        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form): 
        """ Save form data """
        subarea = form.cleaned_data['subareas']
        usuario = Tutor.objects.get(usuario=self.request.user.usuario)
        print(usuario)
        subarea_especialidad = SubAreasEspecialidad()
        subarea_especialidad.tutor = usuario
        subarea_especialidad.subarea = subarea
        subarea_especialidad.save()
        return HttpResponseRedirect(self.get_success_url())

    def post(self, request, *args, **kwargs):
        """ Save subarea new info in D.B. """
        subarea_form = AddSubAreaForm(self.request.POST, request=self.request)

        if subarea_form.is_valid():
            return self.form_valid(subarea_form)
        else:
            return self.form_invalid(subarea_form)

    def get_success_url(self):
        success_url = reverse('tutor:tutor', kwargs={'username': self.request.user.username})
        return str(success_url)


class TutorEditView(LoginRequiredMixin, DetailView):
    """ Tutored edit view. """

    template_name = 'tutor/editar-perfil.html'
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


class SaveEditProfileView(LoginRequiredMixin, FormView):
    template_name = 'tutor/editar-perfil.html'
    form_class = EditProfileTutorForm

    def get_context_data(self, **kwargs):
        """ Add user's extended models to context """
        context = super().get_context_data(**kwargs)
        user = User.objects.get(id=self.request.user.id)
        context['usuario'] = Usuario.objects.get(user=user)
        context['tutor'] = Tutor.objects.get(usuario=context['usuario'])
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
        user_form = EditProfileTutorForm(self.request.POST)

        if user_form.is_valid():
            return self.form_valid(user_form)
        else:
            return self.form_invalid(user_form)

    def get_success_url(self):
        success_url = reverse('tutor:tutor', kwargs={'username': self.request.user.username})
        return str(success_url)


class ChangePasswordView(LoginRequiredMixin, FormView):
    template_name = 'tutor/editar-perfil.html'
    form_class = ChangePasswordForm

    def get_context_data(self, **kwargs):
        """ Add user's extended models to context """
        user = User.objects.get(id=self.request.user.id)
        kwargs['usuario'] = Usuario.objects.get(user=user)
        kwargs['tutor'] = Tutor.objects.get(usuario=kwargs['usuario'])
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
        success_url = reverse('tutor:tutor', kwargs={'username': self.request.user.username})
        return str(success_url)
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs


class ChangeProfilePicView(LoginRequiredMixin, FormView):
    template_name = 'tutor/editar-perfil.html'
    form_class = ChangeProfilePicForm

    def get_context_data(self, **kwargs):
        """ Add user's extended models to context """
        user = User.objects.get(id=self.request.user.id)
        kwargs['usuario'] = Usuario.objects.get(user=user)
        kwargs['tutor'] = Tutor.objects.get(usuario=kwargs['usuario'])
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
        success_url = reverse('tutor:tutor', kwargs={'username': self.request.user.username})
        return str(success_url)


class TutoriasTutorView(LoginRequiredMixin, TemplateView):
    template_name = 'tutor/tutorias.html'


class OfertarHorariosTutorView(LoginRequiredMixin, CreateView):
    pass
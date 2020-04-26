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
from apps.tutorships.models import HorarioTutoria

# Forms
from apps.tutor.forms import EditProfileTutorForm, ChangePasswordForm, \
    ChangeProfilePicForm, AddSubAreaForm, AddHorarioForm

# Utilities
from datetime import datetime, date

# Constants
from doceo.constants import SUBAREAS, TRANSLATE_DAYS

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

    def notificacion(self):
        # Django Channels Notifications Test
        current_user = self.request.user
        channel_layer = get_channel_layer()
        data = 'notification - {}'.format(str(datetime.now()))
        # Trigger message sent to group
        async_to_sync(channel_layer.group_send)(
            str(current_user.id),  # Channel Name, Should always be string
            {
                "type": "notify",   # Custom Function written in the consumers.py
                "text": data,
            },
        )

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


class TutoriasTutorView(LoginRequiredMixin, DetailView):
    template_name = 'tutor/tutorias.html'
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
        context['mis_subareas'] = self.get_mis_subareas()
        context['weekdays'] = self.get_calendario()
        context['horarios'] = self.get_mis_horarios()
        return context

    def get_mis_horarios(self):
        hoy = datetime.today().day
        horarios = HorarioTutoria.objects.filter(tutor=self.request.user.usuario.tutor)
        horarios_validos = []

        for horario in horarios:
            dia = horario.dia
            dia = dia.split(', ')
            if int(dia[1]) >= int(hoy):
                horarios_validos.append(horario)

        return horarios_validos

    def get_mis_subareas(self):
        """ Retrieves user´s subareas stored in DB """
        subareas_guardadas = SubAreasEspecialidad.objects.filter(tutor=self.request.user.usuario.tutor)
        subareas_list = [subarea[1] for subarea in SUBAREAS if subarea[0] == self.request.user.usuario.tutor.area_especialidad]
        mis_subareas = [subareat for subareal in subareas_list for subareat in subareal for sag in subareas_guardadas if sag.subarea == subareat[0]]

        return mis_subareas

    def get_calendario(self):
        """ Returns only week days excludin weekends """
        # Getting current year, month and day
        current_year = datetime.today().year
        current_month = datetime.today().month
        todays_day = datetime.today().day
        # Valiation to check if current motnh is December. If it's December adds 1
        if current_month + 1 > 12:
            number_of_days_in_month = (date((current_year + 1), (current_month + 1), 1) - date(current_year, current_month, 1)).days
        else:
            number_of_days_in_month = (date(current_year, (current_month + 1), 1) - date(current_year, current_month, 1)).days
        # Getting the days left in the month excluding today's day
        days_left = [i for i in range(number_of_days_in_month + 1) if i > todays_day]
        # Getting only work days
        labor_days = []
        for i in days_left:
            week_day = date(current_year, current_month, i).isoweekday()
            if week_day not in [6, 7]:
                labor_days.append({"day": i, "format": f'{TRANSLATE_DAYS[date(current_year, current_month, i).strftime("%A")]}, {i}'})

        return labor_days


class OfertarHorariosTutorView(LoginRequiredMixin, FormView):
    template_name = 'tutor/tutorias.html'
    form_class = AddHorarioForm

    def dispatch(self, request, *args, **kwargs):
        """ This dispatch method helps me to share variables in all the class, e.g. weekdays """
        self.weekdays = [weekday['format'] for weekday in self.get_calendario()]
        if request.method.lower() in self.http_method_names:
            handler = getattr(self, request.method.lower(), self.http_method_not_allowed)
        else:
            handler = self.http_method_not_allowed
        return handler(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """ Add user's extended models to context """
        context = super().get_context_data(**kwargs)
        user = User.objects.get(id=self.request.user.id)
        context['usuario'] = Usuario.objects.get(user=user)
        context['tutor'] = Tutor.objects.get(usuario=context['usuario'])
        context['mis_subareas'] = self.get_mis_subareas()
        context['weekdays'] = self.get_calendario()
        return context

    def form_invalid(self, form):
        """If the form is invalid, render the invalid form."""
        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form): 
        """ Save form data """
        area_especialidad = form.cleaned_data['area_especialidad']
        subarea_especialidad = form.cleaned_data['subarea_especialidad']
        dia = form.cleaned_data['dia']
        hora_inicio = form.cleaned_data['hora_inicio']
        hora_fin = form.cleaned_data['hora_fin']
        lugar = form.cleaned_data['lugar']
        tutor = Tutor.objects.get(usuario=self.request.user.usuario.tutor)
        subarea = SubAreasEspecialidad.objects.get(subarea=subarea_especialidad)
        new_horario = HorarioTutoria.objects.create(tutor=tutor, area_especialidad=area_especialidad, subarea_especialidad=subarea, dia=dia, lugar=lugar, hora_inicio=hora_inicio, hora_final=hora_fin)
        return HttpResponseRedirect(self.get_success_url())

    def post(self, request, *args, **kwargs):
        """ Save subarea new info in D.B. """
        horario_form = AddHorarioForm(self.request.POST, request=self.request, weekdays=self.weekdays)

        if horario_form.is_valid():
            return self.form_valid(horario_form)
        else:
            return self.form_invalid(horario_form)

    def get_success_url(self):
        success_url = reverse('tutor:tutorias', kwargs={'username': self.request.user.username})
        return str(success_url)

    def get_mis_subareas(self):
        """ Retrieves user´s subareas stored in DB """
        subareas_guardadas = SubAreasEspecialidad.objects.filter(tutor=self.request.user.usuario.tutor)
        subareas_list = [subarea[1] for subarea in SUBAREAS if subarea[0] == self.request.user.usuario.tutor.area_especialidad]
        mis_subareas = [subareat for subareal in subareas_list for subareat in subareal for sag in subareas_guardadas if sag.subarea == subareat[0]]

        return mis_subareas

    def get_calendario(self):
        """ Returns only week days excluding weekends """
        TRANSLATE_DAYS = {"Monday": "Lunes", "Tuesday": "Martes", "Wednesday": "Miercoles", "Thursday": "Jueves", "Friday": "Viernes"}
        # Getting current year, month and day
        current_year = datetime.today().year
        current_month = datetime.today().month
        todays_day = datetime.today().day
        # Valiation to check if current motnh is December. If it's December adds 1
        if current_month + 1 > 12:
            number_of_days_in_month = (date((current_year + 1), (current_month + 1), 1) - date(current_year, current_month, 1)).days
        else:
            number_of_days_in_month = (date(current_year, (current_month + 1), 1) - date(current_year, current_month, 1)).days
        # Getting the days left in the month excluding today's day
        days_left = [i for i in range(number_of_days_in_month + 1) if i > todays_day]
        # Getting only work days
        labor_days = []
        for i in days_left:
            week_day = date(current_year, current_month, i).isoweekday()
            if week_day not in [6, 7]:
                labor_days.append({"day": i, "format": f'{TRANSLATE_DAYS[date(current_year, current_month, i).strftime("%A")]}, {i}'})

        return labor_days
# Django
from django import forms
from django.contrib.auth.hashers import check_password
from django.utils.translation import ugettext_lazy as _

# Models
from django.contrib.auth.models import User
from apps.users.models import Usuario
from apps.knowledge_area.models import SubAreasEspecialidad
from apps.tutorships.models import HorarioTutoria
from apps.tutor.models import Tutor

# Constants
from doceo.constants import SUBAREAS


class EditProfileTutorForm(forms.Form):
    """ Edit name and email form """
    nombre = forms.CharField(min_length=4, max_length=80)
    correo = forms.EmailField()
    descripcion = forms.CharField(min_length=10, widget=forms.Textarea(), required=False)


class ChangePasswordForm(forms.Form):
    """ Change user password """

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super().__init__(*args, **kwargs)
    
    curr_password = forms.CharField(max_length=50, widget=forms.PasswordInput(), required=True)
    password = forms.CharField(max_length=50, widget=forms.PasswordInput(), required=True)
    password_confirmation = forms.CharField(max_length=50, widget=forms.PasswordInput(), required=True)

    def clean_curr_password(self):
        current_password = self.cleaned_data['curr_password']

        if current_password == '':
            raise forms.ValidationError('Campo obligatorio')

        return current_password

    def clean(self):
        """ Verify passwords match """

        data = super().clean()

        curr_password = data['curr_password']
        password = data['password']
        password_confirmation = data['password_confirmation']

        user = User.objects.get(id=self.request.user.id)

        if password != password_confirmation:
            raise forms.ValidationError({'password_confirmation': _('Las contraseñas no coinciden')})
        elif not check_password(curr_password, user.password):
            raise forms.ValidationError({'curr_password': _('La contraseña actual no coincide')})

        return data


class ChangeProfilePicForm(forms.ModelForm):
    """ Change user profile picture. """
    class Meta:
        model = Usuario

        fields = ('foto',)

    def clean_foto(self):
        foto = self.cleaned_data['foto']
        extenciones = ['.jpg', '.jpeg', '.png']

        if not foto.name.endswith(tuple(extenciones)):
            raise forms.ValidationError('Formato de archivo invalido. Solo fotos con extencion .jpg, .jpeg o .png')

        return foto


class AddSubAreaForm(forms.Form):

    subareas = forms.ChoiceField(
        choices = (),
        required = False
    )

    def __init__(self, *args, **kwargs):
        self.__subareas = SUBAREAS
        self.request = kwargs.pop("request")
        super(AddSubAreaForm, self).__init__(*args, **kwargs)
        self.subareas_user = [subarea.subarea for subarea in SubAreasEspecialidad.objects.filter(tutor = self.request.user.usuario.tutor)]
        self.subarea_choices = [subarea for subarea in self.__subareas if subarea[0] == self.request.user.usuario.tutor.area_especialidad]
        if len(self.subareas_user) > 0:
            self.fields['subareas'].choices = [subarea for subareas_tuple in self.subarea_choices for subarea in subareas_tuple[1] if subarea[0] not in self.subareas_user]
        else: 
            self.fields['subareas'].choices = [subarea for subareas_tuple in self.subarea_choices for subarea in subareas_tuple[1]]

    def clean_subareas(self):

        subarea = self.cleaned_data['subareas']
        subareas_list = [subarea[1] for subarea in self.__subareas if subarea[0] == self.request.user.usuario.tutor.area_especialidad]
        subareas_aux = [subareas[0] for subareas_tuple in subareas_list for subareas in subareas_tuple]

        if subarea not in subareas_aux:
            raise forms.ValidationError(f'Valor invalido {subarea}.')

        return subarea


class AddHorarioForm(forms.Form):

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        self.weekdays = kwargs.pop("weekdays")
        super().__init__(*args, **kwargs)

    area_especialidad = forms.CharField(max_length=50)
    subarea_especialidad = forms.CharField(max_length=50)
    dia = forms.CharField(max_length=50)
    hora_inicio = forms.TimeField()
    hora_fin = forms.TimeField()
    lugar = forms.CharField(max_length=100)

    def clean_area_especialidad(self):
        area_especialidad = self.cleaned_data['area_especialidad']
        text = area_especialidad.split(' ')
        for i, string in enumerate(text):
            string = string[0].lower() + string[1:]
            text[i] = string
        area_especialidad = ' '.join(text)
        tutor_area_esp = Tutor.objects.get(usuario=self.request.user.usuario)

        if area_especialidad != tutor_area_esp.area_especialidad:
            raise forms.ValidationError('¡La área de especialidad no coincide!')

        return area_especialidad

    def clean_subarea_especialidad(self):
        subarea_especialidad = self.cleaned_data['subarea_especialidad']
        text = subarea_especialidad.split(' ')
        for i, string in enumerate(text):
            string = string[0].lower() + string[1:]
            text[i] = string
        subarea_especialidad = ' '.join(text)
        tutor_subareas = SubAreasEspecialidad.objects.filter(tutor=self.request.user.usuario.tutor)

        for result in tutor_subareas:
            if subarea_especialidad != result.subarea:
                raise forms.ValidationError('¡La subárea no coincide!')

        return subarea_especialidad

    def clean_dia(self):
        dia = self.cleaned_data['dia']
        weekdays = self.weekdays

        if dia not in weekdays:
            raise forms.ValidationError('Escoga un día de los que se muestran en el select')

        return dia

    def clean_lugar(self):
        lugar = self.cleaned_data['lugar']

        if lugar == "":
            raise forms.ValidationError('Campo obligatorio. No dejar en blanco')

        return lugar
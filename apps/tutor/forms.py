# Django
from django import forms
from django.contrib.auth.hashers import check_password
from django.utils.translation import ugettext_lazy as _

# Models
from django.contrib.auth.models import User
from apps.users.models import Usuario
from apps.knowledge_area.models import SubAreasEspecialidad


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
        self.__subareas = (
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
        self.request = kwargs.pop("request")
        super(AddSubAreaForm, self).__init__(*args, **kwargs)
        self.fields['subareas'].choices = [subarea for subarea in self.__subareas if subarea[0] == self.request.user.usuario.tutor.area_especialidad]


    def clean_subareas(self):

        subarea = self.cleaned_data['subareas']
        subareas_list = [subarea[1] for subarea in self.__subareas if subarea[0] == self.request.user.usuario.tutor.area_especialidad]

        for subareas_tuple in subareas_list:
            for subareas in subareas_tuple:
                subareas_aux.append(subareas)
        
        if subarea not in subareas_aux:
            raise forms.ValidationError(f'Valor invalido {subarea}.')

        return subarea
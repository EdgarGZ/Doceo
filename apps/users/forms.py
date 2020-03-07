# Django
from django import forms

# Models
from apps.users.models import Usuario
from apps.tutored.models import Tutorado
from apps.tutor.models import Tutor
from django.contrib.auth.models import User

# Utilidades7
import re
IS_VALID_MAIL =  re.compile(r'^[a-z0-9._%+-]+@[a-z0-9.-]+[\.][a-z]{2,}$')
IS_VALID_EXP = re.compile(r'^[0-9]{2,6}')

# Choices
SEMESTRES = (
    (1, 'Primero'),
    (2, 'Segundo'),
    (3, 'Tercero'),
    (4, 'Cuarto'),
    (5, 'Quinto'),
    (6, 'Sexto'),
    (7, 'Septimo'),
    (8, 'Octavo'),
    (9, 'Noveno'),
)  

CARRERAS = (
    ('Ingenieria de Software', 'SOF'),
    ('Ingenieria en Computacion', 'INC'),
    ('Licenciatura en Informatica', 'INF'),
    ('Ingenieria en Telecomunicaciones y Redes', 'TEL'),
    ('Licenciatura en Administracion de las T.I.', 'ATI'),
) 

AREAS = (
        ('programación', 'Programación'),
        ('matemáticas', 'Matemáticas'),
        ('redes', 'Redes'),
        ('front end', 'Front-End'),
        ('ingles', 'Ingles'),
        ('bases de datos', 'Bases de Datos'),
        ('paralelo', 'Programación en Paralelo'),
        ('imagenes', 'Tratamiento de Imagenes'),
    )


class SignupBaseUserForm(forms.Form):
    """ Signup form """

    username = forms.CharField(min_length=4, max_length=50, widget=forms.TextInput(attrs={'class' : 'form-control'}))
    password = forms.CharField(max_length=70, widget=forms.PasswordInput(attrs={'class' : 'form-control'}))
    password_confirmation = forms.CharField(max_length=70, widget=forms.PasswordInput(attrs={'class' : 'form-control'}))

    def clean_username(self):
        """ Username must be unique """
        username = self.cleaned_data['username']
        username_taken = User.objects.filter(username=username).exists()
        if username_taken:
            raise forms.ValidationError('Username is already in use')
        
        return username

    def clean(self):
        """ Verify password confirmation match """
        data = super().clean()

        password = data['password']
        password_confirmation = data['password_confirmation']

        if password != password_confirmation:
            raise forms.ValidationError('Password do not match')

        return data

    def save(self):
        """ Create new user """
        data = self.cleaned_data
        data.pop('password_confirmation')

        user = User.objects.create_user(**data)


class SignupUserForm(forms.ModelForm):
    class Meta:

        model = Usuario

        fields = (
            'expediente',
            'correo',
            'nombre',
            'foto',
            'descripcion',
        )

        widgets = {
            'expediente': forms.TextInput(attrs={'class' : 'form-control'}),
            'correo': forms.TextInput(attrs={'class' : 'form-control'}),
            'nombre': forms.TextInput(attrs={'class' : 'form-control'}),
            'foto': forms.FileInput(attrs={'class' : 'form-control'}),
            'descripcion': forms.TextInput(attrs={'class' : 'form-control'}),
        }
    
    def clean_expediente(self):
        expediente = self.cleaned_data['expediente']
        
        if not IS_VALID_EXP.match(str(expediente)):
            raise forms.ValidationError('Invalid expedient. Please enter only digits.')
        
        return expediente

    def clean_correo(self):
        correo = self.cleaned_data['correo']
        
        if not IS_VALID_MAIL.match(correo):
            raise forms.ValidationError('Invalid email address. Please check it.')
        
        return correo


class SignupTutoradoForm(forms.ModelForm):
    class Meta:
        model = Tutorado

        fields = ('semestre', 'carrera',)

        widgets = {
            'semestre': forms.Select(choices=SEMESTRES, attrs={'class' : 'form-control'}),
            'carrera': forms.Select(choices=CARRERAS, attrs={'class' : 'form-control'})
        }


class SignupTutorForm(forms.ModelForm):
    class Meta:
        model = Tutor

        fields = ('semestre', 'carrera', 'area_especialidad',)

        widgets = {
            'semestre': forms.Select(choices=SEMESTRES, attrs={'class' : 'form-control'}),
            'carrera': forms.Select(choices=CARRERAS, attrs={'class' : 'form-control'}),
            'area_especialidad': forms.Select(choices=AREAS, attrs={'class' : 'form-control'}),
        }


class PasswordResetRequestForm(forms.Form):
    correo = forms.EmailField()

    def __init__(self, *args, **kwargs):
        super(PasswordResetRequestForm, self).__init__(*args, **kwargs)
        self.fields['correo'].widget.attrs = {'class':'form-control'}


class SetPasswordForm(forms.Form):
    error_messages = {
        'password_mismatch': ("Las contraseñas no coinciden."),
        }
    new_password1 = forms.CharField(label=("Nueva contraseña"),
                                    widget=forms.PasswordInput(attrs={'class':'form-control'}))
    new_password2 = forms.CharField(label=("Confirmar nueva contraseña"),
                                    widget=forms.PasswordInput(attrs={'class':'form-control'}))

    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(
                    self.error_messages['password_mismatch'],
                    code='password_mismatch',
                    )
        return password2
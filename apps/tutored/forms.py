# Django
from django import forms
from django.contrib.auth.hashers import check_password
from django.utils.translation import ugettext_lazy as _

# Models
from django.contrib.auth.models import User
from apps.users.models import Usuario


class EditProfileTutoredForm(forms.Form):
    """ Edit name and email form """
    nombre = forms.CharField(min_length=4, max_length=80)
    correo = forms.EmailField()
    descripcion = forms.CharField(min_length=10, widget=forms.Textarea(), required=False)

    # def clean_descripcion(self):
    #     descripcion = self.cleaned_data['descripcion']
        
    #     if len(descripcion) < 10:
    #         raise forms.ValidationError('La descripción debe contener minimo 10 caracteres')
        
    #     return descripcion


class ChangePasswordForm(forms.Form):
    """ Change user password """

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super().__init__(*args, **kwargs)
    
    curr_password = forms.CharField(max_length=50, widget=forms.PasswordInput())
    password = forms.CharField(max_length=50, widget=forms.PasswordInput())
    password_confirmation = forms.CharField(max_length=50, widget=forms.PasswordInput())

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
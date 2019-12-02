# Django
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Utilidades
import os


# Create your models here.
def get_upload_path_user_image(instance, filename):
    return os.path.join(
        "%s" % instance.user.username, "image_%s" % filename
    )
    
class Usuario(models.Model):
    """
            Modelo Usuario
            Modelo proxy que extiende informacion base con otra
            informacion.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    expediente = models.IntegerField(default=0)
    correo = models.EmailField()
    nombre = models.CharField(max_length=80)
    is_tutor = models.BooleanField(default=False)
    is_tutorado = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_profesor = models.BooleanField(default=False)
    foto = models.ImageField(
        upload_to=get_upload_path_user_image,
        blank=True,
        null=True
    )
    descripcion = models.TextField(blank=True)

    def __str__(self):
        """ Retorna username y nombre """
        return f'Username: {self.user.username} - Name: {self.nombre}'

# Django
from django.db import models

# Models
from apps.tutor.models import Tutor
from apps.knowledge_area.models import SubAreasEspecialidad
from apps.users.models import Usuario



# Create your models here.
class HorarioTutoria(models.Model):
    tutor = models.ForeignKey(Tutor, null=True, blank=True, on_delete=models.CASCADE)
    area_especialidad = models.CharField(max_length=50)
    subarea_especialidad = models.ForeignKey(SubAreasEspecialidad, null=True, blank=True, on_delete=models.CASCADE)
    dia = models.CharField(max_length=35)
    lugar = models.CharField(max_length=100)
    hora_inicio = models.TimeField(auto_now=False, auto_now_add=False, default="04:00:pm")
    hora_final = models.TimeField(auto_now=False, auto_now_add=False, default="04:00:pm")


class NotificacionNuevoHorario(models.Model):
    tutor = models.ForeignKey(Usuario, related_name='noti_tutor', on_delete=models.CASCADE)
    tutorado = models.ForeignKey(Usuario, related_name='noti_tutorado', on_delete=models.CASCADE)
    tutoria = models.ForeignKey(HorarioTutoria, related_name='tutoria', on_delete= models.CASCADE)
    visto_tutorado = models.BooleanField(default=False)
    fecha = models.DateTimeField(auto_now_add=True)
    mensaje = models.CharField(max_length=264, null=True, blank=True)

    def __str__(self):
        return self.id

# class Mensaje(models.Model):
# 	contacto = models.ForeignKey(Contacto, related_name='mensajes', on_delete=models.CASCADE)
# 	contenido = models.TextField()
# 	fecha = models.DateTimeField(auto_now_add=True)

# 	def __str__(self):
# 		return self.contacto.user.username


# class Chat(models.Model):
# 	participantes = models.ManyToManyField(Contacto, related_name='chats')
# 	mensajes = models.ManyToManyField(Mensaje, blank=True)

# 	def __str__(self):
# 		return '{}'.format(self.id)
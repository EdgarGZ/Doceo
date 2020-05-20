# Django
from django.db import models

# Models
from apps.tutor.models import Tutor
from apps.knowledge_area.models import SubAreasEspecialidad
from apps.users.models import Usuario


# Create your models here.
class HorarioTutoria(models.Model):
    """
        Stores a new Turtorship in D.B.
    """
    tutor = models.ForeignKey(Tutor, null=True, blank=True, on_delete=models.CASCADE)
    area_especialidad = models.CharField(max_length=50)
    subarea_especialidad = models.ForeignKey(SubAreasEspecialidad, null=True, blank=True, on_delete=models.CASCADE)
    dia = models.CharField(max_length=35)
    lugar = models.CharField(max_length=100)
    hora_inicio = models.TimeField(auto_now=False, auto_now_add=False, default="04:00:pm")
    hora_final = models.TimeField(auto_now=False, auto_now_add=False, default="04:00:pm")
    disponible = models.BooleanField(default=1)
    en_espera = models.BooleanField(default=0)


# class Tutoria(models.Model):
#     """
#         Stores a new Tutorship scheduled by the tutored
#     """
#     idTutor=models.ForeignKey(Tutor,null=True,blank=True,on_delete=models.CASCADE,related_name='Tutor')
#     idTutorado=models.ForeignKey(Tutorado,null=True,blank=True,on_delete=models.CASCADE,related_name='Tutorado')
#     idHorario=models.ForeignKey(Horarios,null=True,blank=True,on_delete=models.CASCADE,related_name='Horario')
#     idEvidenciaEvaluacion=models.ForeignKey(EvidenciaEvaluacion,null=True,blank=True,on_delete=models.CASCADE,related_name='Evaluacion')
#     idEstadoTutoria=models.ForeignKey(EstadoTutoria,null=True,blank=True,on_delete=models.CASCADE,related_name='Estado')
#     comentarioTutor=models.TextField(blank=True)
#     comentarioTutorado=models.TextField(blank=True)
#     calificacionTutorado=models.FloatField(default=0)
#     duracion=models.CharField(max_length=10,blank=True)
#     fecha = models.CharField(max_length=30, blank=True)
#     comentadoTutorado = models.BooleanField(default=False)


class NotificacionAgendarTutoria(models.Model):
    """
        Stores a new Turtorship Notification in D.B.

        estado options:
            0 -> not accepted: The tutor did not accept the tutorship request
            1 -> pending: the tutorship request is alive (maximum 24 hrs)
            2 -> accepted: the tutor accepted the tutorship request
            3 -> dead: the tutor did not respond the request
    """
    tutor = models.ForeignKey(Usuario, related_name='notificacion_tutor', on_delete=models.CASCADE)
    tutorado = models.ForeignKey(Usuario, related_name='notificacion_tutorado', on_delete=models.CASCADE)
    tutoria = models.ForeignKey(HorarioTutoria, related_name='tutoria', on_delete= models.CASCADE)
    visto_tutorado = models.BooleanField(default=False)
    visto_tutor = models.BooleanField(default=False)
    estado = models.IntegerField()
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'tutoria: {self.tutoria.subarea_especialidad.subarea}'


class EstadoTutoria(models.Model):
    """
        Stores a new Turtorship Notification in D.B.

        estado options:
            0 -> pending: The tutorship is pending.
            1 -> done: the tutorship is done
            2 -> canceled by tutor: the tutor canceled the tutorship
            3 -> canceled by tutored: the tutored canceled the tutorship
    """
    estado = models.IntegerField(default=0)
    motivo = models.TextField(blank=True)
    # vistoTutor = models.BooleanField(default=0)
    # vistoTutorado = models.BooleanField(default=0)


class Tutoria(models.Model):
    tutor = models.ForeignKey(Usuario, null=True, blank=True, on_delete=models.CASCADE, related_name='tutor_tutoria')
    tutorado = models.ForeignKey(Usuario, null=True, blank=True, on_delete=models.CASCADE, related_name='tutorado_tutoria')
    tutoria = models.ForeignKey(HorarioTutoria, null=True, blank=True, on_delete=models.CASCADE, related_name='horario_tutoria')
    estado_tutoria = models.ForeignKey(EstadoTutoria, null=True, blank=True, on_delete=models.CASCADE, related_name='estado_tutoria')
    fecha = models.CharField(max_length=60, blank=True)


class TutoresTutorado(models.Model):
    tutor = models.ForeignKey(Usuario, null=True, blank = True, on_delete=models.CASCADE, related_name='tutores_tutorado_tutor')
    tutorado = models.ForeignKey(Usuario, null=True, blank=True, on_delete=models.CASCADE, related_name='tutores_tutorado_tutorado')
    fecha = models.DateTimeField(auto_now_add=True)
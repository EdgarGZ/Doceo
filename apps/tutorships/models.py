# Django
from django.db import models

# Models
from apps.tutor.models import Tutor


# Create your models here.
class HorarioTutoria(models.Model):
    tutor = models.ForeignKey(Tutor, null=True, blank=True, on_delete=models.CASCADE)
    # categoria=models.ForeignKey(
    #     Categoria, 
    #     on_delete = models.CASCADE,
    #     blank=True,
    #     unique=False
    # )
    dia = models.CharField(max_length=15)
    lugar = models.CharField(max_length=100)
    hora_inicio = models.TimeField(auto_now=False, auto_now_add=False, default="04:00:pm")
    hora_final = models.TimeField(auto_now=False, auto_now_add=False, default="04:00:pm")
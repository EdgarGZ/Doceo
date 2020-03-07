# Django
from django.db import models

# Models
from apps.tutor.models import Tutor


class SubAreasEspecialidad(models.Model):
    tutor = models.ForeignKey(
        Tutor,
        blank=True,
        null=True,
        on_delete=models.CASCADE
    )
    subarea = models.CharField(
        max_length = 30,
    )
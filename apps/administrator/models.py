# Django
from django.db import models

# Models
from apps.users.models import Usuario

# Create your models here.
class Admin(models.Model):
	usuario=models.OneToOneField(
		Usuario, 
		on_delete = models.CASCADE,
        blank = True,
		primary_key = True
	)
	facultad=models.CharField(max_length=30)
# Django
from django.db import models

# Models
from apps.users.models import Usuario


# Create your models here.
class Tutorado(models.Model):
	usuario=models.OneToOneField(
		Usuario, 
		on_delete = models.CASCADE,
		blank=True,
		primary_key=True
	)

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
	semestre=models.SmallIntegerField(
		choices=SEMESTRES,
		default=1
	)

	CARRERAS = (
        ('Ingenieria de Software', 'SOF'),
        ('Ingenieria en Computacion', 'INC'),
        ('Licenciatura en Informatica', 'INF'),
        ('Ingenieria en Telecomunicaciones y Redes', 'TEL'),
        ('Licenciatura en Administracion de las T.I.', 'ATI'),
    ) 
	carrera=models.CharField(
		max_length=50,
		choices=CARRERAS,
		default='Ingenieria de Software'
	)

	def __str__(self):
		return self.usuario.user.username
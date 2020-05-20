# Celery
from celery import shared_task

# Django
from django.core.mail import send_mail

# Models
from apps.tutorships.models import HorarioTutoria
from django.contrib.auth.models import User

# Constants
from doceo.constants import SUBAREAS
from doceo.settings import DEFAULT_FROM_EMAIL


# Functions
def get_verbose_name(text):
    only_subareas_array = [subarea[1] for subarea in SUBAREAS]
    subarea = [subarea[1] for subareas in only_subareas_array for subarea in subareas if subarea[0] == text]
    return subarea[0]

@shared_task
def notify_tutored_by_email(tutor_id, tutored_id, tutorship_id):
    tutorship = HorarioTutoria.objects.get(id=tutorship_id)
    tutor = User.objects.get(id=tutor_id)
    tutored = User.objects.get(id=tutored_id)

    tutorship_name = get_verbose_name(tutorship.subarea_especialidad.subarea)
    subject = f'New tutorship request for {tutorship_name} on Doceo'
    message = f'Hey {tutor.username}, the Doceo team have news for you!\n\n{tutored.username} ({tutored.usuario.correo}) wants to take your tutorship {tutorship_name}!\n\nGo to www.doceo.com and let {tutored.username} know if you wanna give your tutorship to her/him.'
    # Mandar email
    send_mail(subject, message, DEFAULT_FROM_EMAIL, [tutor.usuario.correo])

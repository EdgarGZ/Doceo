# Generated by Django 2.2.6 on 2020-05-19 01:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tutorships', '0007_auto_20200518_1935'),
    ]

    operations = [
        migrations.RenameField(
            model_name='notificacionagendartutoria',
            old_name='vistp_tutor',
            new_name='visto_tutor',
        ),
    ]

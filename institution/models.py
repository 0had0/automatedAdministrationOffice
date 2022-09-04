from django.db import models

from .manager import InstitutionManager


class Institution(models.Model):
    institution_id = models.AutoField(primary_key=True, unique=True)

    name = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True, blank=True, null=True, verbose_name='email', default='')
    phone_number = models.IntegerField(default=-1)

    creation_time = models.DateField(auto_now_add=True)

    objects = InstitutionManager()

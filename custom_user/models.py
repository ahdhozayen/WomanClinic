from django.db import models
from django.contrib.auth.models import AbstractUser
from clinic.models import Clinic

class User(AbstractUser):
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE,blank=True, null=True, related_name='user_clinic', verbose_name='أسم المستشفي')

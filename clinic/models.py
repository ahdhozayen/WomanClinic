from django.db import models
from django.utils.translation import ugettext_lazy as _

class Clinic(models.Model):
    clinic_name = models.CharField(max_length=50)

    def __str__(self):
        return self.clinic_name

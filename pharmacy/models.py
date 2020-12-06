from django.conf import settings
from django.db import models
from datetime import date
from django.utils.translation import ugettext_lazy as _


class Medicine(models.Model):
    scientific_name =  models.CharField(max_length=80, verbose_name=_('Scientific Name'))
    trade_name =  models.CharField(max_length=80, verbose_name=_('Trade Name'))
    alternate1 = models.CharField(max_length=80, blank=True, null=True, verbose_name=_('Alternate1'))
    alternate2 = models.CharField(max_length=80, blank=True, null=True, verbose_name=_('Alternate2'))
    start_date  = models.DateField(auto_now=False, auto_now_add=False, default=date.today, verbose_name=_('Start Date'))
    end_date    = models.DateField(auto_now=False, auto_now_add=False, blank=True, null=True, verbose_name=_('End Date'))
    created_by  = models.ForeignKey(settings.AUTH_USER_MODEL, blank=False, on_delete=models.CASCADE, related_name="medicine_created_by")
    creation_date = models.DateField(auto_now=True, auto_now_add=False)
    last_update_by = models.ForeignKey(settings.AUTH_USER_MODEL, blank=False, on_delete=models.CASCADE, related_name="medicine_last_updated_by")
    last_update_date = models.DateField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return self.trade_name

from django.conf import settings
from django.db import models
from datetime import date
from django.utils.translation import ugettext_lazy as _
from patient.models import Patient
from clinic.models import Clinic

class Surgery_Master(models.Model):
    surgery_name =  models.CharField(max_length=80, verbose_name=_('Sergry Name'))
    start_date  = models.DateField(auto_now=False, auto_now_add=False, default=date.today, verbose_name=_('Start Date'))
    end_date    = models.DateField(auto_now=False, auto_now_add=False, blank=True, null=True, verbose_name=_('End Date'))
    created_by  = models.ForeignKey(settings.AUTH_USER_MODEL, blank=False, on_delete=models.CASCADE, related_name="surgery_master_created_by")
    creation_date = models.DateField(auto_now=True, auto_now_add=False)
    last_update_by = models.ForeignKey(settings.AUTH_USER_MODEL, blank=False, on_delete=models.CASCADE, related_name="surgery_master_last_updated_by")
    last_update_date = models.DateField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return self.surgery_name

class Surgery_Steps(models.Model):
    sergry_master = models.ForeignKey(Surgery_Master, on_delete=models.CASCADE, verbose_name=_('Sergry Name'))
    step_name =  models.CharField(max_length=80, verbose_name=_('Step'))
    start_date  = models.DateField(auto_now=False, auto_now_add=False, default=date.today, verbose_name=_('Start Date'))
    end_date    = models.DateField(auto_now=False, auto_now_add=False, blank=True, null=True, verbose_name=_('End Date'))
    created_by  = models.ForeignKey(settings.AUTH_USER_MODEL, blank=False, on_delete=models.CASCADE, related_name="surgery_patient_created_by")
    creation_date = models.DateField(auto_now=True, auto_now_add=False)
    last_update_by = models.ForeignKey(settings.AUTH_USER_MODEL, blank=False, on_delete=models.CASCADE, related_name="surgery_patient_updated_by")
    last_update_date = models.DateField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return self.step_name

class Surgery_Doctor(models.Model):
    doctor_name =  models.CharField(max_length=120, null=True, blank=True, verbose_name=_('Doctor Name'))
    hospital = models.ForeignKey(Clinic, on_delete=models.CASCADE, verbose_name=_('Hospital'))
    created_by  = models.ForeignKey(settings.AUTH_USER_MODEL, blank=False, on_delete=models.CASCADE, related_name="surgery_doc_created_by")
    creation_date = models.DateField(auto_now=True, auto_now_add=False)
    last_update_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.CASCADE, related_name="surgery_doc_updated_by")
    last_update_date = models.DateField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return self.doctor_name

class Patient_Surgery(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, blank=True, null=True, verbose_name=_('Patient'))
    surgery_name = models.ForeignKey(Surgery_Master, on_delete=models.CASCADE, verbose_name=_('Sergry Name'))
    surgery_doctor = models.ForeignKey(Surgery_Doctor, on_delete=models.CASCADE, verbose_name=_('Surgery Doctor'))
    surgery_date  = models.DateField(auto_now=False, auto_now_add=False, default=date.today, verbose_name=_('Surgery Date'))
    exit_date  = models.DateField(auto_now=False, auto_now_add=False, default=date.today, verbose_name=_('Exit Date'))
    case_progress = models.CharField(max_length=250, blank=True, null=True, verbose_name=_('Progress'))
    final_diagnosis = models.CharField(max_length=250, blank=True, null=True, verbose_name=_('Final Diagnosis'))
    recomendations = models.TextField(blank=True, null=True,verbose_name=_('Recomendations'))
    start_date  = models.DateField(auto_now=False, auto_now_add=False, default=date.today, verbose_name=_('Start Date'))
    end_date    = models.DateField(auto_now=False, auto_now_add=False, blank=True, null=True, verbose_name=_('End Date'))
    created_by  = models.ForeignKey(settings.AUTH_USER_MODEL, blank=False, on_delete=models.CASCADE, related_name="surgery_steps_created_by")
    creation_date = models.DateField(auto_now=True, auto_now_add=False)
    last_update_by = models.ForeignKey(settings.AUTH_USER_MODEL, blank=False, on_delete=models.CASCADE, related_name="surgery_steps_updated_by")
    last_update_date = models.DateField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return self.surgery_name+" "+self.patient.name

class After_Surgery(models.Model):
    surgery = models.ForeignKey(Patient_Surgery, on_delete=models.CASCADE, blank=True, null=True, verbose_name=_('Surgery'))
    after_surgery_notes = models.TextField(blank=True, null=True,verbose_name=_('After Surgery Notes'))
    after_surgery_recomendations = models.TextField(blank=True, null=True,verbose_name=_('After Surgery Recomendations'))
    follow_up_date  = models.DateField(auto_now=False, auto_now_add=False, default=date.today, verbose_name=_('Follow Up Date'))
    created_by  = models.ForeignKey(settings.AUTH_USER_MODEL, blank=False, on_delete=models.CASCADE, related_name="after_surgery_created_by")
    creation_date = models.DateField(auto_now=True, auto_now_add=False)
    last_update_by = models.ForeignKey(settings.AUTH_USER_MODEL, blank=False, on_delete=models.CASCADE, related_name="after_surgery_updated_by")
    last_update_date = models.DateField(auto_now=False, auto_now_add=True)

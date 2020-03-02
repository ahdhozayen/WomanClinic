from django.conf import settings
from django.db import models
from datetime import date
from django.utils.translation import ugettext_lazy as _
from patient.models import Patient
from clinic.models import Clinic

class Surgery_Master(models.Model):
    surgery_name =  models.CharField(max_length=80, verbose_name='نوع العملية')
    start_date  = models.DateField(auto_now=False, auto_now_add=False, default=date.today, verbose_name=_('Start Date'))
    end_date    = models.DateField(auto_now=False, auto_now_add=False, blank=True, null=True, verbose_name=_('End Date'))
    created_by  = models.ForeignKey(settings.AUTH_USER_MODEL, blank=False, on_delete=models.CASCADE, related_name="surgery_master_created_by")
    creation_date = models.DateField(auto_now=True, auto_now_add=False)
    last_update_by = models.ForeignKey(settings.AUTH_USER_MODEL, blank=False, on_delete=models.CASCADE, related_name="surgery_master_last_updated_by")
    last_update_date = models.DateField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return self.surgery_name

class Surgery_Steps(models.Model):
    sergry_master = models.ForeignKey(Surgery_Master, on_delete=models.CASCADE, verbose_name='نوع العملية')
    step_name =  models.CharField(max_length=80, verbose_name='الخطوات')
    start_date  = models.DateField(auto_now=False, auto_now_add=False, default=date.today, verbose_name=_('Start Date'))
    end_date    = models.DateField(auto_now=False, auto_now_add=False, blank=True, null=True, verbose_name=_('End Date'))
    created_by  = models.ForeignKey(settings.AUTH_USER_MODEL, blank=False, on_delete=models.CASCADE, related_name="surgery_patient_created_by")
    creation_date = models.DateField(auto_now=True, auto_now_add=False)
    last_update_by = models.ForeignKey(settings.AUTH_USER_MODEL, blank=False, on_delete=models.CASCADE, related_name="surgery_patient_updated_by")
    last_update_date = models.DateField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return self.step_name

class Surgery_Doctor(models.Model):
    doctor_name =  models.CharField(max_length=120, null=True, blank=True, verbose_name='اسم الدكتور')
    hospital = models.ForeignKey(Clinic, on_delete=models.CASCADE, verbose_name='المستشفي')
    created_by  = models.ForeignKey(settings.AUTH_USER_MODEL, blank=False, on_delete=models.CASCADE, related_name="surgery_doc_created_by")
    creation_date = models.DateField(auto_now=True, auto_now_add=False)
    last_update_by = models.ForeignKey(settings.AUTH_USER_MODEL, blank=False, on_delete=models.CASCADE, related_name="surgery_doc_updated_by")
    last_update_date = models.DateField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return self.doctor_name

class Patient_Surgery(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, verbose_name='اسم المريضة')
    surgery_name = models.ForeignKey(Surgery_Master, on_delete=models.CASCADE, verbose_name='نوع العملية')
    surgery_doctor = models.ForeignKey(Surgery_Doctor, on_delete=models.CASCADE, verbose_name='اسم الجراح')
    surgery_date  = models.DateField(auto_now=False, auto_now_add=False, default=date.today, verbose_name='تاريخ اجراء العملية')
    exit_date  = models.DateField(auto_now=False, auto_now_add=False, default=date.today, verbose_name='تاريخ الخروج')
    case_progress = models.CharField(max_length=250, blank=True, null=True, verbose_name='تطور الحالة')
    final_diagnosis = models.CharField(max_length=250, blank=True, null=True, verbose_name='التشخيص النهائي')
    recomendations = models.TextField(blank=True, null=True,verbose_name='توصيات اخري')
    start_date  = models.DateField(auto_now=False, auto_now_add=False, default=date.today, verbose_name=_('Start Date'))
    end_date    = models.DateField(auto_now=False, auto_now_add=False, blank=True, null=True, verbose_name=_('End Date'))
    created_by  = models.ForeignKey(settings.AUTH_USER_MODEL, blank=False, on_delete=models.CASCADE, related_name="surgery_steps_created_by")
    creation_date = models.DateField(auto_now=True, auto_now_add=False)
    last_update_by = models.ForeignKey(settings.AUTH_USER_MODEL, blank=False, on_delete=models.CASCADE, related_name="surgery_steps_updated_by")
    last_update_date = models.DateField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return self.patient.name

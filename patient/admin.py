from django.contrib import admin
from patient.models import Patient, Delivery, Check_Up, Patient_Files


class Delivery_Admin_Inline(admin.TabularInline):
    model = Delivery

class Check_Up_Admin_Inline(admin.TabularInline):
    model = Check_Up

class Patient_Files_Admin_Inline(admin.TabularInline):
    model = Patient_Files


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    models = Patient
    inlines=[Delivery_Admin_Inline,Check_Up_Admin_Inline,Patient_Files_Admin_Inline]

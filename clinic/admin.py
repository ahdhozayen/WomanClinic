from django.contrib import admin
from clinic.models import Clinic

@admin.register(Clinic)
class ClinicAdmin(admin.ModelAdmin):
    models = Clinic

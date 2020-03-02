from django.contrib import admin
from surgery import models

class Surgery_Steps_Inline(admin.TabularInline):
    model = models.Surgery_Steps

@admin.register(models.Surgery_Master)
class Surgery_master_Admin(admin.ModelAdmin):
    model = models.Surgery_Master
    inlines = [
               Surgery_Steps_Inline,
    ]

@admin.register(models.Patient_Surgery)
class Surgery_master_Admin(admin.ModelAdmin):
    model = models.Patient_Surgery

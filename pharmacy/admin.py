from django.contrib import admin
from pharmacy.models import Medicine

@admin.register(Medicine)
class Medicine_Admin(admin.ModelAdmin):
    model = Medicine

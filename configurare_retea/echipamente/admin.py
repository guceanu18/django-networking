from django.contrib import admin
from .models import Echipament, Router, InterfataRouter

# Register your models here.
@admin.register(Echipament)
class EchipamentAdmin(admin.ModelAdmin):
    list_display = ('id', 'nume', 'ip', 'tip', 'utilizator')  # Coloanele care vor fi afișate

@admin.register(Router)
class RouterAdmin(admin.ModelAdmin):
    list_display = ('id', 'nume', 'ip_mgmt')

@admin.register(InterfataRouter)
class InterfataRouterAdmin(admin.ModelAdmin):
    list_display = ('id', 'nume_interfata', 'ip', 'router')
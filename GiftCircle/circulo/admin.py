from django.contrib import admin

# Register your models here.
from .models import Circulo, Persona, Deseo

admin.site.register(Circulo)
admin.site.register(Persona)
admin.site.register(Deseo)

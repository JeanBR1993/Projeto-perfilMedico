from django.contrib import admin
from django.forms import RadioSelect
from .models import Paciente, documentoMedico, pesoAltura, hemogramaCompleto, Glicemia, funcaoRenal, funcaoHepatica, funcaoTireoide, marcadoresInflamacao, Anemia, Hormonais, DSTs, Sorologias
from django.db import models

class DSTsAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.BooleanField: {'widget': RadioSelect(choices=[(True, 'Positivo'), (False, 'Negativo')])},
    }

class SorologiaAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.BooleanField: {'widget': RadioSelect(choices=[(True, 'Positivo'), (False, 'Negativo')])},
    }


# Register your models here.
admin.site.register(Paciente)
admin.site.register(documentoMedico)
admin.site.register(pesoAltura)
admin.site.register(hemogramaCompleto)
admin.site.register(Glicemia)
admin.site.register(funcaoRenal)
admin.site.register(funcaoHepatica)
admin.site.register(funcaoTireoide)
admin.site.register(marcadoresInflamacao)
admin.site.register(Anemia)
admin.site.register(Hormonais)
admin.site.register(DSTs, DSTsAdmin)
admin.site.register(Sorologias, SorologiaAdmin)



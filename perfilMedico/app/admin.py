from django.contrib import admin
from django.forms import RadioSelect
from django.db import models
from .models import Vacina, CID, FichaCadastral, Prontuario,HistoricoPesoAltura, ExameLaboratorial, Vacinas, Medicamento, Medico, Receituario, MedicamentoReceitado


# Register your models here.

admin.site.register(Vacina)
admin.site.register(FichaCadastral)
admin.site.register(Prontuario)
admin.site.register(HistoricoPesoAltura)
admin.site.register(ExameLaboratorial)
admin.site.register(Vacinas)
admin.site.register(Medicamento)
admin.site.register(Medico)
admin.site.register(MedicamentoReceitado)
admin.site.register(CID)
admin.site.register(Receituario)
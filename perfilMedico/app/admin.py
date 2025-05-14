from django.contrib import admin
from django import forms
from .models import Vacina, CID, FichaCadastral, Prontuario,HistoricoPesoAltura, ExameLaboratorial, Medicamento, Medico, Receituario, MedicamentoReceitado, RegistroVacinacao


class prontuarioForm(forms.ModelForm):
    doador = forms.ChoiceField(
        choices=[(True, 'Sim'), (False, 'Não')],
        widget=forms.Select()
    )

    class Meta:
        model = Prontuario
        fields = '__all__'

class prontuarioAdmin(admin.ModelAdmin):
    form = prontuarioForm

class ExameLaboratorialAdminForm(forms.ModelForm):
    class Meta:
        model = ExameLaboratorial
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Transforma TODOS os campos booleanos em RadioSelect
        for field_name, field in self.fields.items():
            if isinstance(field, forms.BooleanField) or isinstance(field, forms.NullBooleanField):
                # Substitui o widget diretamente, em vez de modificar choices
                if field.required:
                    # Para campos obrigatórios (sem null)
                    field.widget = forms.RadioSelect(choices=[
                        (True, 'Sim'), 
                        (False, 'Não')
                    ])
                else:
                    # Para campos que permitem null
                    field.widget = forms.RadioSelect(choices=[
                        (True, 'Sim'), 
                        (False, 'Não'),
                        (None, '-----')
                    ])

class ExameLaboratorialAdmin(admin.ModelAdmin):
    form = ExameLaboratorialAdminForm



# Register your models here.

admin.site.register(Vacina)
admin.site.register(FichaCadastral)
admin.site.register(Prontuario, prontuarioAdmin)
admin.site.register(HistoricoPesoAltura)
admin.site.register(ExameLaboratorial, ExameLaboratorialAdmin)
admin.site.register(RegistroVacinacao)
admin.site.register(Medicamento)
admin.site.register(Medico)
admin.site.register(MedicamentoReceitado)
admin.site.register(CID)
admin.site.register(Receituario)
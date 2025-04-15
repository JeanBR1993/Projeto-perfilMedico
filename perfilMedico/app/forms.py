from django import forms
from django.forms import RadioSelect
from .models import DSTs, Sorologias

class DSTsForm(forms.ModelForm):
    hiv = forms.BooleanField(
        widget=RadioSelect(choices=[(True, 'Positivo'), (False, 'Negativo')]),
        required=False,
        label="Resultado do teste HIV")

    vdrlOUrpr = forms.BooleanField(
        widget=RadioSelect(choices=[(True, 'Positivo'), (False, 'Negativo')]),
        required=False,
        label="Resultado do teste Sífilis Triagem VDRL ou  RPR")

    ftaabsOUtpha = forms.BooleanField(
        widget=RadioSelect(choices=[(True, 'Positivo'), (False, 'Negativo')]),
        required=False,
        label="Resultado do teste Sífilis FTA-ABS ou TPHA")

    hbsag = forms.BooleanField(
        widget=RadioSelect(choices=[(True, 'Positivo'), (False, 'Negativo')]),
        required=False,
        label="Resultado do teste HBSAG")

    antihbv = forms.BooleanField(
        widget=RadioSelect(choices=[(True, 'Positivo'), (False, 'Negativo')]),
        required=False,
        label="Resultado do teste Anti HBV")

    antihcv = forms.BooleanField(
        widget=RadioSelect(choices=[(True, 'Positivo'), (False, 'Negativo')]),
        required=False,
        label="Resultado do teste Anti HCV")

    sorologiaHerpesIGC = forms.BooleanField(
        widget=RadioSelect(choices=[(True, 'Positivo'), (False, 'Negativo')]),
        required=False,
        label="Resultado do teste Herpes IGC")

    sorologiaHerpesIGM = forms.BooleanField(
        widget=RadioSelect(choices=[(True, 'Positivo'), (False, 'Negativo')]),
        required=False,
        label="Resultado do teste Herpes IGM")

    clamidia = forms.BooleanField(
        widget=RadioSelect(choices=[(True, 'Positivo'), (False, 'Negativo')]),
        required=False,
        label="Resultado do teste Clamídia")

    gonorreia = forms.BooleanField(
        widget=RadioSelect(choices=[(True, 'Positivo'), (False, 'Negativo')]),
        required=False,
        label="Resultado do teste Gonorreia")

    class Meta:
        model = DSTs
        fields = ['data', 'paciente', 'hiv', 'vdrlOUrpr', 'ftaabsOUtpha', 'hbsag', 'antihbv', 'antihcv', 'sorologiaHerpesIGC', 'sorologiaHerpesIGM', 'clamidia', 'gonorreia', 'arquivoExame']


class SorologiasForm(forms.ModelForm):
    dengue = forms.BooleanField(
        widget=RadioSelect(choices=[(True, 'Positivo'), (False, 'Negativo')]),
        required=False,
        label="Resultado do teste Dengue")

    zikaVirus = forms.BooleanField(
        widget=RadioSelect(choices=[(True, 'Positivo'), (False, 'Negativo')]),
        required=False,
        label="Resultado do teste ZikaVirus")

    chikungunya = forms.BooleanField(
        widget=RadioSelect(choices=[(True, 'Positivo'), (False, 'Negativo')]),
        required=False,
        label="Resultado do teste Chikungunya")

    febreTifoide = forms.BooleanField(
        widget=RadioSelect(choices=[(True, 'Positivo'), (False, 'Negativo')]),
        required=False,
        label="Resultado do teste Febre Tifoide")

    toxoplasmose = forms.BooleanField(
        widget=RadioSelect(choices=[(True, 'Positivo'), (False, 'Negativo')]),
        required=False,
        label="Resultado do teste Toxoplasmose")

    rubeola = forms.BooleanField(
        widget=RadioSelect(choices=[(True, 'Positivo'), (False, 'Negativo')]),
        required=False,
        label="Resultado do teste Rubeola")

    citomegalovirus = forms.BooleanField(
        widget=RadioSelect(choices=[(True, 'Positivo'), (False, 'Negativo')]),
        required=False,
        label="Resultado do teste Citomegalovirus")

    chagas = forms.BooleanField(
        widget=RadioSelect(choices=[(True, 'Positivo'), (False, 'Negativo')]),
        required=False,
        label="Resultado do teste Chagas")

    leptospirose = forms.BooleanField(
        widget=RadioSelect(choices=[(True, 'Positivo'), (False, 'Negativo')]),
        required=False,
        label="Resultado do teste Leptospirose")

    fatorReumatoide = forms.BooleanField(
        widget=RadioSelect(choices=[(True, 'Positivo'), (False, 'Negativo')]),
        required=False,
        label="Resultado do teste Fator Reumatóide")

    antiCCP = forms.BooleanField(
        widget=RadioSelect(choices=[(True, 'Positivo'), (False, 'Negativo')]),
        required=False,
        label="Resultado do teste AntiCCP")

    anticorpoAntinuclear = forms.BooleanField(
        widget=RadioSelect(choices=[(True, 'Positivo'), (False, 'Negativo')]),
        required=False,
        label="Resultado do teste Anticorpo Antinuclear")

    antiDNA = forms.BooleanField(
        widget=RadioSelect(choices=[(True, 'Positivo'), (False, 'Negativo')]),
        required=False,
        label="Resultado do teste AntiDNA ")

    ebv = forms.BooleanField(
        widget=RadioSelect(choices=[(True, 'Positivo'), (False, 'Negativo')]),
        required=False,
        label="Resultado do teste EBV")

    covid19 = forms.BooleanField(
        widget=RadioSelect(choices=[(True, 'Positivo'), (False, 'Negativo')]),
        required=False,
        label="Resultado do teste Covid19")

    class Meta:
        model = Sorologias
        fields = ['data', 'paciente', 'dengue', 'zikaVirus', 'chikungunya', 'febreTifoide', 'toxoplasmose', 'rubeola', 'citomegalovirus', 'chagas', 'leptospirose', 'fatorReumatoide',  'antiCCP', 'anticorpoAntinuclear', 'antiDNA', 'ebv', 'covid19', 'arquivoExame']
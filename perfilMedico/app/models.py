from django.db import models
from django.core.validators import RegexValidator, MinLengthValidator
from django.core.exceptions import ValidationError
from django.utils import timezone

from datetime import timedelta


def validadorDeCPF(numeroSTR):
    n10 = 10
    n11 = 11
    soma1 = 0
    soma2 = 0
    for char in numeroSTR[:9]:
        soma1 += int(char) * n10
        n10 -= 1
    
    validacao1 = soma1 * 10
    validacao1 = validacao1 % 11
    if  validacao1 != int(numeroSTR[9:10]):
        raise ValidationError("Número de CPF inexistente, primeiro dígito verificador inválido")
    
    for char in numeroSTR[:10]:
        soma2 += int(char) * n11
        n11 -= 1
    
    validacao2 = soma2 * 10
    validacao2 = validacao2 % 11
    if  validacao2 != int(numeroSTR[10:11]):
        raise ValidationError("Número de CPF inexistente, segundo dígito verificador inválido")

def validadorDataNascimento(value):
    today = timezone.now().date()
    min_date = today - timedelta(days=150*365)  # 150 anos
    max_date = today  
    
    if value < min_date:
        raise ValidationError(f"Data de nascimento não pode ser menor do que {min_date}")
    if value > max_date:
        raise ValidationError("Data de nascimento não pode ser no futuro")

listaGenerosNascimento = [
    ('H', 'Homem'),
    ('M', 'Mulher'),
]

listaTiposSanguineos = [
    ('A+','A+'), 
    ('A-','A-'),
    ('B+','B+'), 
    ('B-','B-'),
    ('AB+','AB+'), 
    ('AB-','AB-'),
    ('O+','O+'),
    ('O-','O-') 
]

# Create your models here.
class Paciente(models.Model):

    cpf = models.CharField(
        max_length=11,
        unique=True,
        validators=[RegexValidator(regex=r'^\d{11}$',message='Número de CPF precisa ter apenas números e 11 deles.',code='cpf_invalido'), validadorDeCPF]
    )

    numeroSUS = models.PositiveIntegerField(
        unique=True
    )

    nome = models.CharField(
        max_length=100,
        blank=False,
        validators=[MinLengthValidator(5)]
    )

    cep = models.CharField(
        max_length=8,
        validators=[RegexValidator(regex=r'\d{8}$', message='Número de CEP ter apenas números e 8 deles.', code='cep_invalido')],
        blank = False
    )

    endereço = models.CharField(
        max_length=100,
        blank = False
    )

    dataNascimento = models.DateField(
        blank=False,
        validators=[validadorDataNascimento],
        help_text="Data de nascimento pode estar entre 0 dias e 150 anos atrás."
    )

    generoNascimento = models.CharField(
        max_length=1,
        choices=listaGenerosNascimento,
        default="H",
        blank=False
    )

    generoIdentificação = models.CharField(
        max_length=20,
        blank = True
    )

    tipoSanguineo = models.CharField(
        max_length=3,
        choices=listaTiposSanguineos,
        blank=False
    )


    def __str__(self):
        return self.nome + " - " + "CPF: " + str(self.cpf) + " - " + "número SUS: " + str(self.numeroSUS)
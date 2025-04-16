from django.db import models
from django.core.validators import RegexValidator, MinLengthValidator, MinValueValidator, MaxValueValidator, FileExtensionValidator
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

class CID(models.Model):

    codigo = models.CharField(
        max_length = 8,
        unique=True,  
        help_text="Código da doença",
        verbose_name="CID"
    )

    descricao = models.CharField(
        max_length=50,
        unique=True,
        help_text="Descrição da doença",
    )

    def __str__(self):
        return self.descricao

class Remedio(models.Model):
    compostoAtivo = models.CharField(
        max_length = 50,
        blank=False,
        null=False,
        verbose_name="Composto ativo"
    )

    dosagem = models.DecimalField(
        decimal_places=2,
        max_digits=10,
        blank=False,
        null=False,
        verbose_name="Dosagem"
    )


# Create your models here.
class Paciente(models.Model):

    cpf = models.CharField(
        max_length=11,
        unique=True,
        validators=[RegexValidator(regex=r'^\d{11}$',message='Número de CPF precisa ter apenas números e 11 deles.',code='cpf_invalido'), validadorDeCPF],
        help_text="Somente números",
        verbose_name="CPF"
    )

    numeroSUS = models.PositiveIntegerField(
        unique=True,
        help_text="Somente números",
        verbose_name="Número do SUS"
    )

    nome = models.CharField(
        max_length=100,
        blank=False,
        validators=[MinLengthValidator(5)],
        verbose_name="Nome completo"
    )

    cep = models.CharField(
        max_length=8,
        validators=[RegexValidator(regex=r'\d{8}$', message='Número de CEP ter apenas números e 8 deles.', code='cep_invalido')],
        blank = False,
        help_text="Somente números",
        verbose_name="CEP"
    )

    endereço = models.CharField(
        max_length=100,
        blank = False,
        verbose_name="Endereço de residência"
    )

    dataNascimento = models.DateField(
        blank=False,
        validators=[validadorDataNascimento],
        verbose_name="Data de Nascimento",
        help_text="Data de nascimento no formato DD/MM/AAAA"
    )

    generoNascimento = models.CharField(
        max_length=1,
        choices=listaGenerosNascimento,
        default="H",
        blank=False,
        verbose_name="Gênero de Nascimento"
    )

    generoIdentificação = models.CharField(
        max_length=20,
        blank = True,
        verbose_name="Gênero de Identificação"
    )

    tipoSanguineo = models.CharField(
        max_length=3,
        choices=listaTiposSanguineos,
        blank=False,
        verbose_name="Tipo Sanguíneo"
    )

    cid = models.ForeignKey(
        CID,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="Código CID"
    )

    def __str__(self):
        return self.nome

# classes de implementação dos arquivos de documento médico,
# falta a tomada de decisão por qual serviço de hospedagem,
# se Amazon S3, Microsoft Azure e etc...
"""class PrivateMedicalStorage():
    location = 'private'
    default_acl = 'private'
    file_overwrite = False
    custom_domain = False"""

# tem bastante coisa pra fazer e melhorar nesse objeto
# tem que automatizar a obtenção do tipo de arquivo
class documentoMedico(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name="documentos")
    arquivo = models.FileField(
        upload_to='uploads/',
        validators=[FileExtensionValidator(allowed_extensions=["pdf", "jpeg"])],
        help_text="Aceita apenas PDF e JPEG"
    )
    descrição = models.CharField(max_length=255)
    data_upload = models.DateTimeField(auto_now_add=True)
    tipo_arquivo = models.CharField(max_length=10)  # 'pdf', 'jpeg', etc.
    
    # Additional medical metadata
    tipoDocumento = models.CharField(max_length=50, verbose_name="Tipo de documento", blank=True, null=True)  # 'xray', 'lab_report', etc.
    anotacaoMedico = models.TextField(blank=True, verbose_name="Anotação do Médico")
    
    class Meta:
        indexes = [
            models.Index(fields=['paciente', 'data_upload']),
            models.Index(fields=['tipo_arquivo']),
        ]
    
    class Meta:
        verbose_name = "Documento médico"
        verbose_name_plural = "Documentos médicos"

    def __str__(self):
        return self.descrição+self.tipo_arquivo+ " - " + str(self.paciente)[:10]

class pesoAltura(models.Model):
    data = models.DateField(
        null=False,
        blank=False,
        help_text="Data de obtenção dos dados",
        verbose_name="Data"
    )
    
    peso = models.DecimalField(
        max_digits=4,
        decimal_places=1,
        validators=[MinValueValidator(0), MaxValueValidator(400.0)],
        blank=False,
        help_text="Em kilogramas"
    )

    altura = models.IntegerField(
        blank=False,
        validators=[MinValueValidator(20), MaxValueValidator(280)],
        help_text="Em centímetros"
    )

    paciente = models.ForeignKey(
        Paciente,
        on_delete=models.CASCADE,
        verbose_name="Paciente"
    )

    class Meta:
        verbose_name = "Peso e altura do paciente"
        verbose_name_plural = "Peso e altura dos pacientes"
    
    def __str__(self):
        return str(self.paciente)

class hemogramaCompleto(models.Model):
    data = models.DateField(
        null=False,
        blank=False,
        help_text="Data de obtenção dos dados",
        verbose_name="Data"
    )

    paciente = models.ForeignKey(
        Paciente,
        on_delete=models.CASCADE,
        verbose_name="Paciente"
    )

# Série Vermelha
    hemoglobina = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        validators=[MinValueValidator(0), MaxValueValidator(40.0)],
        blank=True,
        help_text="g/dL",
        null=True
    )

    hematocrito = models.SmallIntegerField(
        validators=[MinValueValidator(0)],
        blank=True,
        help_text="porcentagem",
        null=True
    )

    hemacias = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        validators=[MinValueValidator(0), MaxValueValidator(30.0)],
        blank=True,
        help_text="milhões/uL",
        null=True
    )

    volumeCorpuscular = models.DecimalField(
        max_digits=4,
        decimal_places=1,
        validators=[MinValueValidator(0), MaxValueValidator(999.0)],
        blank=True,
        help_text="f/L",
        verbose_name="Volume Corpuscular Médio",
        null=True
    )

    hemoglobinaCorpuscular = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        validators=[MinValueValidator(0), MaxValueValidator(99.0)],
        blank=True,
        help_text="pg",
        verbose_name="Hemoglobina Corpuscular Média",
        null=True
    )

    concentracaoHemoglobinaCorpuscular = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        validators=[MinValueValidator(0), MaxValueValidator(99.0)],
        blank=True,
        help_text="g/dL",
        verbose_name="Concentração Hemoglobina Corpuscular Média",
        null=True
    )

    amplitudeEritrocitos = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        validators=[MinValueValidator(0), MaxValueValidator(99.0)],
        blank=True,
        help_text="porcentagem",
        verbose_name="Amplitude de Distribuição dos Eritrócitos",
        null=True
    )

# Série Branca
    leucocitosTotais  = models.PositiveSmallIntegerField(
        blank=True,
        help_text="µL",
        verbose_name="Leucócitos totais",
        null=True
    )

    neutrofilos  = models.PositiveSmallIntegerField(
        blank=True,
        help_text="µL",
        verbose_name="Neutrófilos",
        null=True
    )

    linfocitos  = models.PositiveSmallIntegerField(
        blank=True,
        help_text="µL",
        verbose_name="Linfócitos",
        null=True
    )

    monocitos  = models.PositiveSmallIntegerField(
        blank=True,
        help_text="µL",
        verbose_name="Monócitos",
        null=True
    )

    eosinofilos  = models.PositiveSmallIntegerField(
        blank=True,
        help_text="µL",
        verbose_name="Eosinófilos",
        null=True
    )

    basofilos = models.PositiveSmallIntegerField(
        blank=True,
        help_text="µL",
        verbose_name="Basófilos",
        null=True
    )

# Plaquetas

    plaquetas = models.PositiveIntegerField(
        blank=True,
        help_text="µL",
        verbose_name="Plaquetas (PLT)",
        null=True
    )

    volumePlaquetario = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        blank=True,
        help_text="fL",
        verbose_name="Volume Plaquetário Médio (VPM)",
        null=True
    )

    # ---------------------------------------------------------------
    arquivoExame = models.ForeignKey(documentoMedico, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Arquivo do exame")

    class Meta:
        verbose_name = "Hemograma Completo"
        verbose_name_plural = "Hemogramas Completos"
    
    def __str__(self):
        return str(self.paciente)

class Glicemia(models.Model):
    data = models.DateField(
        null=False,
        blank=False,
        help_text="Data de obtenção dos dados",
        verbose_name="Data"
    )

    paciente = models.ForeignKey(
        Paciente,
        on_delete=models.CASCADE,
        verbose_name="Paciente"
    )

    glicemiaJejum = models.PositiveSmallIntegerField(
        blank=True,
        help_text="mg/dL",
        verbose_name="Glicemia em jejum",
        null=True
    )

    hemoglobinaGlicada = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        validators=[MinValueValidator(0), MaxValueValidator(100.0)],
        blank=True,
        help_text="porcentagem",
        verbose_name = "Hemoglobina Glicada (HbA1c)",
        null=True
    )

    arquivoExame = models.ForeignKey(documentoMedico, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Arquivo do exame")

    class Meta:
        verbose_name = "Glicemia"
        verbose_name_plural = "Glicemias"

    def __str__(self):
        return str(self.paciente)

class funcaoRenal(models.Model):
    data = models.DateField(
        null=False,
        blank=False,
        help_text="Data de obtenção dos dados",
        verbose_name="Data"
    )

    paciente = models.ForeignKey(
        Paciente,
        on_delete=models.CASCADE,
        verbose_name="Paciente"
    )    

    creatinina = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        validators=[MinValueValidator(0),MaxValueValidator(100)],
        help_text="mg/dL",
        blank=True,
        null=True
    )

    ureia = models.DecimalField(
        max_digits=4,
        decimal_places=1,
        validators=[MinValueValidator(0),MaxValueValidator(999)],
        help_text="mg/dL",
        blank=True,
        null=True
    )

    filtracaoGlomerular = models.DecimalField(
        max_digits=4,
        decimal_places=1,
        validators=[MinValueValidator(0),MaxValueValidator(999)],
        help_text="mL/min/1,73 m²",
        blank=True,
        verbose_name="Taxa de Filtração Glomerular (TFG ou eGFR)",
        null=True
    )

    acidoUrico = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        validators=[MinValueValidator(0),MaxValueValidator(99)],
        help_text="mg/dL",
        blank=True,
        verbose_name="Ácido Úrico",
        null=True
    )

    sodio = models.DecimalField(
        max_digits=4,
        decimal_places=1,
        validators=[MinValueValidator(0),MaxValueValidator(999)],
        help_text="mEq/L",
        blank=True,
        verbose_name="Sódio (Na⁺)",
        null=True
    )

    potassio = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        validators=[MinValueValidator(0),MaxValueValidator(99)],
        help_text="mEq/L",
        blank=True,
        verbose_name="Potássio (K⁺)",
        null=True
    )

    calcio = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        validators=[MinValueValidator(0),MaxValueValidator(99)],
        help_text="mEq/L",
        blank=True,
        verbose_name="Cálcio (Ca²⁺)",
        null=True
    )

    fosforo = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        validators=[MinValueValidator(0),MaxValueValidator(99)],
        help_text="mEq/L",
        blank=True,
        verbose_name="Fósforo (P)",
        null=True
    )

    arquivoExame = models.ForeignKey(documentoMedico, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Arquivo do exame")

    class Meta:
        verbose_name = "Função Renal"
        verbose_name_plural = "Funções Renais"
    
    def __str__(self):
        return str(self.paciente)

class funcaoHepatica(models.Model):
    data = models.DateField(
        null=False,
        blank=False,
        help_text="Data de obtenção dos dados",
        verbose_name="Data"
    )

    paciente = models.ForeignKey(
        Paciente,
        on_delete=models.CASCADE,
        verbose_name="Paciente"
    )

    alt = models.SmallIntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(0)],
        help_text="U/L",
        verbose_name="Alanina Aminotransferase (ALT)"
    )

    ast = models.SmallIntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(0)],
        help_text="U/L",
        verbose_name="Aspartato Aminotransferase (AST)"
    )

    fa = models.SmallIntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(0)],
        help_text="U/L",
        verbose_name="Fosfatase Alcalina (FA)"
    )

    ggt = models.SmallIntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(0)],
        help_text="U/L",
        verbose_name="Gama-Glutamil Transferase (GGT)"
    )

    bilirrubinaTotal = models.DecimalField(
        decimal_places=1,
        max_digits=3,
        null=True,
        blank=True,
        validators=[MinValueValidator(0)],
        help_text="mg/dL",
        verbose_name="Bilirrubina Total"
    )

    albumina = models.DecimalField(
        decimal_places=1,
        max_digits=3,
        null=True,
        blank=True,
        validators=[MinValueValidator(0)],
        help_text="g/dL",
        verbose_name="Albumina"
    )

    tempoProtrombina = models.DecimalField(
        decimal_places=1,
        max_digits=3,
        null=True,
        blank=True,
        validators=[MinValueValidator(0)],
        help_text="Em segundos",
        verbose_name="TP (Tempo de Protrombina) / INR"
    )

    amonia = models.DecimalField(
        decimal_places=1,
        max_digits=3,
        null=True,
        blank=True,
        validators=[MinValueValidator(0)],
        help_text=" µg/dL",
        verbose_name="Amônia"
    )

    ldh = models.SmallIntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(0)],
        help_text="U/L",
        verbose_name="Desidrogenase Láctica (LDH)"
    )

    arquivoExame = models.ForeignKey(documentoMedico, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Arquivo do exame")

    class Meta:
        verbose_name = "Função Hepática"
        verbose_name_plural = "Funções Hepáticas"
    
    def __str__(self):
        return str(self.paciente)

class funcaoTireoide(models.Model):
    data = models.DateField(
        null=False,
        blank=False,
        help_text="Data de obtenção dos dados",
        verbose_name="Data"
    )

    paciente = models.ForeignKey(
        Paciente,
        on_delete=models.CASCADE,
        verbose_name="Paciente"
    )

    tsh = models.DecimalField(
        decimal_places=1,
        max_digits=3,
        null=True,
        blank=True,
        validators=[MinValueValidator(0)],
        help_text="mUI/L",
        verbose_name="Hormônio Tireoestimulante (TSH)"
    )

    t4 = models.DecimalField(
        decimal_places=1,
        max_digits=3,
        null=True,
        blank=True,
        validators=[MinValueValidator(0)],
        help_text="ng/dL",
        verbose_name="Tiroxina Livre (T4)"
    )

    t3 = models.DecimalField(
        decimal_places=1,
        max_digits=3,
        null=True,
        blank=True,
        validators=[MinValueValidator(0)],
        help_text="pg/mL",
        verbose_name="Triiodotironina Livre (T3)"
    )

    t4Total = models.DecimalField(
        decimal_places=1,
        max_digits=3,
        null=True,
        blank=True,
        validators=[MinValueValidator(0)],
        help_text="µg/dL",
        verbose_name="Tiroxina Total (T4 Total)"
    )

    t3Total = models.DecimalField(
        decimal_places=1,
        max_digits=3,
        null=True,
        blank=True,
        validators=[MinValueValidator(0)],
        help_text="ng/dL",
        verbose_name="Triiodotironina Total (T3 Total)"
    )

    antiTPO = models.SmallIntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(0)],
        help_text="UI/mL",
        verbose_name="Anticorpo Antiperoxidase Tireoidiana (Anti-TPO)"
    )

    antiTG = models.SmallIntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(0)],
        help_text="UI/mL",
        verbose_name="Anticorpo Antitireoglobulina (Anti-Tg)"
    )

    trab = models.SmallIntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(0)],
        help_text="UI/L",
        verbose_name="Anticorpo Antirreceptor de TSH (TRAb)"
    )

    arquivoExame = models.ForeignKey(documentoMedico, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Arquivo do exame")
    class Meta:
        verbose_name = "Parâmetros Tireoide"
        verbose_name_plural = "Parâmetros Tireoides"
    
    def __str__(self):
        return str(self.paciente)

class marcadoresInflamacao(models.Model):
    data = models.DateField(
        null=False,
        blank=False,
        help_text="Data de obtenção dos dados",
        verbose_name="Data"
    )

    paciente = models.ForeignKey(
        Paciente,
        on_delete=models.CASCADE,
        verbose_name="Paciente"
    )

    pcr = models.DecimalField(
        decimal_places=1,
        max_digits=3,
        null=True,
        blank=True,
        validators=[MinValueValidator(0)],
        help_text="mg/dL",
        verbose_name="Proteína C-Reativa (PCR)"
    )

    evhs = models.SmallIntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(0)],
        help_text="mm/h",
        verbose_name="Velocidade de Hemossedimentação (VHS)"
    )

    arquivoExame = models.ForeignKey(documentoMedico, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Arquivo do exame")
    class Meta:
        verbose_name = "Marcadores de Inflamação"
        verbose_name_plural = "Marcadores de Inflamações"
    
    def __str__(self):
        return str(self.paciente)

class Anemia(models.Model):
    data = models.DateField(
        null=False,
        blank=False,
        help_text="Data de obtenção dos dados",
        verbose_name="Data"
    )
    
    paciente = models.ForeignKey(
        Paciente,
        on_delete=models.CASCADE,
        verbose_name="Paciente"
    )

    ferritinina = models.SmallIntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(0)],
        help_text="ng/mL",
        verbose_name="Ferritina"
    )

    ferroSerico = models.SmallIntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(0)],
        help_text="µg/dL",
        verbose_name="Ferro Sérico"
    )

    arquivoExame = models.ForeignKey(documentoMedico, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Arquivo do exame")

    class Meta:
        verbose_name = "Marcadores de Anemia"
        verbose_name_plural = "Marcadores de Anemias"
    
    def __str__(self):
        return str(self.paciente)

class Hormonais(models.Model):
    data = models.DateField(
        null=False,
        blank=False,
        help_text="Data de obtenção dos dados",
        verbose_name="Data"
    )

    paciente = models.ForeignKey(
        Paciente,
        on_delete=models.CASCADE,
        verbose_name="Paciente"
    )

    estradiol = models.SmallIntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(0)],
        help_text="pg/dL",
        verbose_name="Estradiol (E2)"
    )

    progesterona = models.SmallIntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(0)],
        help_text="ng/mL",
        verbose_name="Progesterona"
    )

    fsh = models.SmallIntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(0)],
        help_text="mIU/mL",
        verbose_name="Hormônio Folículoestimulante (FSH)"
    )

    lh = models.SmallIntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(0)],
        help_text="mIU/mL",
        verbose_name="Hormônio Luteinizante (LH)"
    )

    testosteronaTotal = models.SmallIntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(0)],
        help_text="ng/dL",
        verbose_name="Testosterona Total"
    )

    testosteronaLivre = models.SmallIntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(0)],
        help_text="ng/dL",
        verbose_name="Testosterona Livre"
    )

    cortisol = models.SmallIntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(0)],
        help_text="µg/dL",
        verbose_name="Cortisol (8h da manhã)"
    )

    acth = models.SmallIntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(0)],
        help_text="pg/dL",
        verbose_name="Hormônio Adrenocorticotrófico (ACTH)"
    )

    aldosterona = models.SmallIntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(0)],
        help_text="ng/dL",
        verbose_name="Aldosterona (em repouso)"
    )

    peptideoC = models.DecimalField(
        decimal_places=1,
        max_digits=3,
        null=True,
        blank=True,
        validators=[MinValueValidator(0)],
        help_text="ng/dL",
        verbose_name="Peptídeo C"
    )

    prolactina = models.SmallIntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(0)],
        help_text="ng/dL",
        verbose_name="prolactina"
    )

    gh = models.DecimalField(
        decimal_places=1,
        max_digits=3,
        null=True,
        blank=True,
        validators=[MinValueValidator(0)],
        help_text="ng/mL",
        verbose_name="Hormônio do Crescimento (GH)"
    )

    arquivoExame = models.ForeignKey(documentoMedico, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Arquivo do exame")
    class Meta:
        verbose_name = "Taxa Hormonal"
        verbose_name_plural = "Taxas Hormonais"
    
    def __str__(self):
        return str(self.paciente)

class DSTs(models.Model):
    data = models.DateField(
        null=False,
        blank=False,
        help_text="Data de obtenção dos dados",
        verbose_name="Data"
    )

    paciente = models.ForeignKey(
        Paciente,
        on_delete=models.CASCADE,
        verbose_name="Paciente"
    )

    hiv = models.BooleanField(
        null=True,
        blank=True,
        help_text="reativo?",
        verbose_name="HIV"
    )
    
    vdrlOUrpr = models.BooleanField(
        null=True,
        blank=True,
        help_text="reativo?",
        verbose_name="VDRL/RPR"
    )

    ftaabsOUtpha = models.BooleanField(
        null=True,
        blank=True,
        help_text="reativo?",
        verbose_name="FTA-ABS/TPHA"
    )

    hbsag = models.BooleanField(
        null=True,
        blank=True,
        help_text="reativo?",
        verbose_name="HBsAg"
    )

    antihbc = models.BooleanField(
        null=True,
        blank=True,
        help_text="reativo?",
        verbose_name="Anti-HBc"
    )
    
    antihbs = models.BooleanField(
        null=True,
        blank=True,
        help_text="reativo?",
        verbose_name="Anti-HBs"
    )

    antihcv = models.BooleanField(
        null=True,
        blank=True,
        help_text="reativo?",
        verbose_name="Anti-HCV"
    )

    sorologiaHerpesIGC = models.BooleanField(
        null=True,
        blank=True,
        help_text="reativo?",
        verbose_name="Sorologia Herpes IgC"
    )

    sorologiaHerpesIGM = models.BooleanField(
        null=True,
        blank=True,
        help_text="reativo?",
        verbose_name="Sorologia Herpes IgM"
    )


    clamidia = models.BooleanField(
        null=True,
        blank=True,
        help_text="reativo?",
        verbose_name="Clamídia"
    )

    gonorreia = models.BooleanField(
        null=True,
        blank=True,
        help_text="reativo?",
        verbose_name="Gonorreia"
    )
    arquivoExame = models.ForeignKey(documentoMedico, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Arquivo do exame")
    
    class Meta:
        verbose_name = "Sorologias de DST"
        verbose_name_plural = "Sorologias de DSTs"
    
    def __str__(self):
        return str(self.paciente)

class Sorologias(models.Model):
    data = models.DateField(
        null=False,
        blank=False,
        help_text="Data de obtenção dos dados",
        verbose_name="Data"
    )

    paciente = models.ForeignKey(
        Paciente,
        on_delete=models.CASCADE,
        verbose_name="Paciente"
    )

    dengue = models.BooleanField(
        null=True,
        blank=True,
        help_text="reativo?",
        verbose_name="Dengue"
    )

    zikaVirus = models.BooleanField(
        null=True,
        blank=True,
        help_text="reativo?",
        verbose_name="Zika Virus"
    )

    chikungunya = models.BooleanField(
        null=True,
        blank=True,
        help_text="reativo?",
        verbose_name="Chikungunya"
    )
    
    febreTifoide = models.BooleanField(
        null=True,
        blank=True,
        help_text="reativo?",
        verbose_name="Febre Tifoide"
    )

    toxoplasmose = models.BooleanField(
        null=True,
        blank=True,
        help_text="reativo?",
        verbose_name="Toxoplasmose"
    )

    rubeola = models.BooleanField(
        null=True,
        blank=True,
        help_text="reativo?",
        verbose_name="Rubeola"
    )

    citomegalovirus = models.BooleanField(
        null=True,
        blank=True,
        help_text="reativo?",
        verbose_name="Citomegalovírus"
    )

    chagas = models.BooleanField(
        null=True,
        blank=True,
        help_text="reativo?",
        verbose_name="Doença de Chagas"
    )
    
    leptospirose = models.BooleanField(
        null=True,
        blank=True,
        help_text="reativo?",
        verbose_name="Leptospirose"
    )

    fatorReumatoide = models.BooleanField(
        null=True,
        blank=True,
        help_text="reativo?",
        verbose_name="Fator Reumatoide"
    )

    antiCCP = models.BooleanField(
        null=True,
        blank=True,
        help_text="reativo?",
        verbose_name="Anti-CCP"
    )
    
    anticorpoAntinuclear = models.BooleanField(
        null=True,
        blank=True,
        help_text="reativo?",
        verbose_name="Anticorpo Antinuclear"
    )
    
    antiDNA = models.BooleanField(
        null=True,
        blank=True,
        help_text="reativo?",
        verbose_name="Anti-DNA dupla hélice"
    )

    ebv = models.BooleanField(
        null=True,
        blank=True,
        help_text="reativo?",
        verbose_name="Epstein-Barr Vírus"
    )

    covid19 = models.BooleanField(
        null=True,
        blank=True,
        help_text="reativo?",
        verbose_name="Covid19"
    )

    arquivoExame = models.ForeignKey(documentoMedico, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Arquivo do exame")

    class Meta:
        verbose_name = "Outras Sorologias"
        verbose_name_plural = "Outras Sorologias"
    
    def __str__(self):
        return str(self.paciente)
    
class Receituario(models.Model):

    data = models.DateField(
        null=False,
        blank=False,
        help_text="Data de emissão receituário",
        verbose_name="Data"
    )

    paciente = models.ForeignKey(
        Paciente,
        on_delete=models.CASCADE,
        verbose_name="Paciente"
    )

    remedio = models.ForeignKey(
        Remedio,
        on_delete=models.CASCADE,
        verbose_name="Remedio",
        blank=True,
        default=None
    )

    cid = models.ForeignKey(
        CID,
        on_delete=models.CASCADE,
        verbose_name="Código da doença"
    )

    crm = models.CharField(
        max_length=15,
        blank=False,
        verbose_name="CRM do médico"
    )

    nomeDoMedico = models.CharField(
        max_length=50,
        blank=False,
        verbose_name="Nome do médico"
    )

    textoReceituario = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name="Texto do receituário, período de tratamento, sugestão de uso"
    )

    def __str__(self):
        return str(self.data) + " - " + str(self.paciente) + " - " + str(self.cid)
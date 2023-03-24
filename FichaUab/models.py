import uuid
from django.db import models

# Create your models here.
class Pessoa(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nome = models.CharField(max_length=255)
    cpf = models.CharField(max_length=14, unique=True)
    email = models.EmailField()
    data_nascimento = models.DateField()

class Endereco(models.Model):
    cep = models.CharField(max_length=8)
    logradouro = models.CharField(max_length=255)
    numero = models.CharField(max_length=15)
    complemento = models.CharField(max_length=31, null=True, blank=True)
    referencia = models.CharField(max_length=63, null=True, blank=True)
    bairro = models.CharField(max_length=127)
    cidade = models.CharField(max_length=127)
    estado = models.CharField(max_length=2)

class DadosBancarios(models.Model):
    pessoa = models.ForeignKey(Pessoa, on_delete=models.CASCADE)
    banco = models.CharField(max_length=127)
    agencia = models.CharField(max_length=31)
    conta = models.CharField(max_length=31)
    operacao = models.CharField(max_length=7, null=True, blank=True)

class Mantenedor(models.Model):
    nome = models.CharField(max_length=255)
    responsavel = models.CharField(max_length=255)
    cnpj = models.CharField(max_length=18)
    endereco = models.ForeignKey(Endereco, on_delete=models.SET_NULL, null=True)
    telefone = models.CharField(max_length=15)
    email = models.EmailField()
    tipo = models.CharField(max_length=15, choices=(('Municipal', 'Municipal'), ('Estadual', 'Estadual')))

class Polo(models.Model):
    CLASSIFICACAO_SEED_CHOICES = (
        ('L', 'L - Polo com interrupção de entrada de estudantes nos cursos que necessitam de laboratório'),
        ('R', 'R - Polo com interrupção de entrada de estudantes'),
        ('S', 'S - Polo com infraestrutura suficiente'),
        ('T', 'T - Polo com recomendação de melhoria')
    )
    
    nome = models.CharField(max_length=255)
    endereco = models.ForeignKey(Endereco, on_delete=models.SET_NULL, null=True)
    email_institucional = models.EmailField()
    telefone = models.CharField(max_length=15)
    ativo = models.BooleanField()
    classificacao_seed = models.CharField(max_length=1, choices=CLASSIFICACAO_SEED_CHOICES)
    possui_biblioteca_municipal = models.BooleanField()
    coordenador = models.ForeignKey(Pessoa, on_delete=models.RESTRICT)
    latitude = models.FloatField()
    longitude = models.FloatField()
    apresentacao = models.TextField()

class Curso(models.Model):
    TIPO_DE_CURSO_CHOICES = (
        ('Graduação (Bacharelado)', 'Graduação (Bacharelado)'),
        ('Graduação (Licenciatura)', 'Graduação (Licenciatura)'),
        ('Extensão', 'Extensão'),
        ('Especialização', 'Especialização'),
        ('Aperfeiçoamanto', 'Aperfeiçoamento'),
        ('Tecnólogo', 'Tecnólogo')
    )

    nome = models.CharField(max_length=255)
    tipo_de_curso = models.CharField(max_length=127, choices=TIPO_DE_CURSO_CHOICES)
    email_curso = models.EmailField()
    telefone_curso = models.CharField(max_length=15)
    coordenador = models.ForeignKey(Pessoa, on_delete=models.RESTRICT)
    ativo = models.BooleanField()
    descricao = models.TextField()
    perfil_egresso = models.TextField()

    def __str__(self):
        return self.nome

class Disciplina(models.Model):
    TIPO_DISCIPLINA_CHOICES = (
        ('Disciplina Convencional', 'Disciplina Convencional'),
        ('TCC', 'Trabalho de Conclusão de Curso'),
        ('Estágio Predominantemente Prático', 'Estágio Predominantemente Prático')
    )
    
    nome = models.CharField(max_length=255)
    carga_horaria = models.IntegerField()
    tipo_disciplina = models.CharField(max_length=55)
    curso = models.ForeignKey(Curso, on_delete=models.SET_NULL, null=True)

class PessoaFichaUab(models.Model):
    BOLSA_REQUERIDA_CHOICES = (
        ('COORDENADOR UAB I', 'COORDENADOR UAB I'),
        ('COORDENADOR ADJUNTO UAB I', 'COORDENADOR ADJUNTO UAB I'),
        ('COORDENADOR DE TUTORIA I', 'COORDENADOR DE TUTORIA I'),
        ('PROFESSOR REVISOR I', 'PROFESSOR REVISOR I'),
        ('PROFESSOR REVISOR II', 'PROFESSOR REVISOR II'),
        ('TUTOR A DISTÂNCIA', 'TUTOR A DISTÂNCIA'),
        ('PROFESSOR FORMADOR I', 'PROFESSOR FORMADOR I'),
        ('PROFESSOR FORMADOR II', 'PROFESSOR FORMADOR II'),
        ('PROFESSOR CONTEUDISTA I', 'PROFESSOR CONTEUDISTA I'),
        ('PROFESSOR CONTEUDISTA II', 'PROFESSOR CONTEUDISTA II'),
        ('COORDENADOR DE CURSO I', 'COORDENADOR DE CURSO I'),
        ('ASSISTENTE À DOCÊNCIA', 'ASSISTENTE À DOCÊNCIA'),
        ('TUTOR PRESENCIAL', 'TUTOR PRESENCIAL')
    )

    ESTADO_CIVIL_CHOICES = (
        ('Solteiro(a)', 'Solteiro(a)'),
        ('Casado(a)', 'Casado(a)'),
        ('Separado(a)', 'Separado(a)'),
        ('Divorciado(a)', 'Divorciado(a)'),
        ('Viúvo(a)', 'Viúvo(a)'),
        ('União Estável', 'União Estável')
    )

    ULTIMO_CURSO_SUPERIOR_CHOICES = (
        ('Exatas', 'Exatas'),
        ('Biológicas', 'Biológicas'),
        ('Humanas', 'Humanas')
    )
    
    pessoa = models.ForeignKey(Pessoa, on_delete=models.CASCADE)
    curso_vinculado = models.ForeignKey(Curso, on_delete=models.SET_NULL, null=True)
    bolsa_requerida = models.CharField(max_length=31, choices=BOLSA_REQUERIDA_CHOICES)
    sexo = models.CharField(max_length=1, choices=(('M', 'Masculino'), ('F', 'Feminino')))
    profissao = models.CharField(max_length=127)
    tipo_documento = models.CharField(max_length=3, choices=(('RG', 'RG'), ('CNH', 'CNH')))
    numero_documento = models.CharField(max_length=31)
    orgao_expeditor = models.CharField(max_length=15)
    data_emissao = models.DateField()
    uf_nascimento = models.CharField(max_length=2)
    municipio_nascimento = models.CharField(max_length=255)
    estado_civil = models.CharField(max_length=15, choices=ESTADO_CIVIL_CHOICES)
    nome_conjuge = models.CharField(max_length=255, null=True, blank=True)
    nome_pai = models.CharField(max_length=255, null=True, blank=True)
    nome_mae = models.CharField(max_length=255)
    endereco = models.ForeignKey(Endereco, on_delete=models.SET_NULL, null=True)
    telefone = models.CharField(max_length=15)
    area_ultimo_curso_superior = models.CharField(max_length=10, choices=ULTIMO_CURSO_SUPERIOR_CHOICES)
    ultimo_curso_titulacao = models.CharField(max_length=127)
    instituicao_titulacao = models.CharField(max_length=127)
    dados_bancarios = models.ForeignKey(DadosBancarios, on_delete=models.SET_NULL, null=True)
    data_inicio_vinculacao = models.DateField()
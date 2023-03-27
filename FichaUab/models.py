import uuid
from django.db import models

# Create your models here.
class Pessoa(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nome = models.CharField(max_length=255)
    cpf = models.CharField(max_length=14, unique=True, verbose_name='CPF')
    email = models.EmailField(verbose_name='E-mail')
    data_nascimento = models.DateField(verbose_name='Data de Nascimento')

class Endereco(models.Model):
    cep = models.CharField(max_length=8, verbose_name='CEP')
    logradouro = models.CharField(max_length=255)
    numero = models.CharField(max_length=15, verbose_name='Número')
    complemento = models.CharField(max_length=31, null=True, blank=True)
    referencia = models.CharField(max_length=63, null=True, blank=True, verbose_name='Referência')
    bairro = models.CharField(max_length=127)
    cidade = models.CharField(max_length=127)
    estado = models.CharField(max_length=2)

class DadosBancarios(models.Model):
    pessoa = models.ForeignKey(Pessoa, on_delete=models.CASCADE)
    banco = models.CharField(max_length=127)
    agencia = models.CharField(max_length=31, verbose_name='Agência')
    conta = models.CharField(max_length=31)
    operacao = models.CharField(max_length=7, null=True, blank=True, verbose_name='Operação')

class Mantenedor(models.Model):
    nome = models.CharField(max_length=255)
    responsavel = models.CharField(max_length=255, verbose_name='Responsável')
    cnpj = models.CharField(max_length=18, verbose_name='CNPJ')
    endereco = models.ForeignKey(Endereco, on_delete=models.SET_NULL, null=True, verbose_name='Endereço')
    telefone = models.CharField(max_length=15)
    email = models.EmailField(verbose_name='E-mail')
    tipo = models.CharField(max_length=15, choices=(('Municipal', 'Municipal'), ('Estadual', 'Estadual')))

class Polo(models.Model):
    CLASSIFICACAO_SEED_CHOICES = (
        ('L', 'L - Polo com interrupção de entrada de estudantes nos cursos que necessitam de laboratório'),
        ('R', 'R - Polo com interrupção de entrada de estudantes'),
        ('S', 'S - Polo com infraestrutura suficiente'),
        ('T', 'T - Polo com recomendação de melhoria')
    )
    
    nome = models.CharField(max_length=255)
    endereco = models.ForeignKey(Endereco, on_delete=models.SET_NULL, null=True, verbose_name='Endereço')
    email_institucional = models.EmailField(verbose_name='E-mail Institucional')
    telefone = models.CharField(max_length=15)
    ativo = models.BooleanField()
    classificacao_seed = models.CharField(max_length=1, choices=CLASSIFICACAO_SEED_CHOICES, verbose_name='Classificação SEED')
    possui_biblioteca_municipal = models.BooleanField(verbose_name='Possui Biblioteca Municipal?')
    coordenador = models.ForeignKey(Pessoa, on_delete=models.RESTRICT)
    latitude = models.FloatField()
    longitude = models.FloatField()
    apresentacao = models.TextField(verbose_name='Apresentação')

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
    tipo_de_curso = models.CharField(max_length=127, choices=TIPO_DE_CURSO_CHOICES, verbose_name='Tipo de Curso')
    email_curso = models.EmailField(verbose_name='E-mail do Curso')
    telefone_curso = models.CharField(max_length=15, verbose_name='Telefone do Curso')
    coordenador = models.ForeignKey(Pessoa, on_delete=models.RESTRICT)
    ativo = models.BooleanField()
    descricao = models.TextField(verbose_name='Descrição')
    perfil_egresso = models.TextField(verbose_name='Perfil do Egresso')

    def __str__(self):
        return self.nome

class Disciplina(models.Model):
    TIPO_DISCIPLINA_CHOICES = (
        ('Disciplina Convencional', 'Disciplina Convencional'),
        ('TCC', 'Trabalho de Conclusão de Curso'),
        ('Estágio Predominantemente Prático', 'Estágio Predominantemente Prático')
    )
    
    nome = models.CharField(max_length=255)
    carga_horaria = models.IntegerField(verbose_name='Carga Horária')
    tipo_disciplina = models.CharField(max_length=55, verbose_name='Tipo de Disciplina')
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
    curso_vinculado = models.ForeignKey(Curso, on_delete=models.SET_NULL, null=True, verbose_name='Curso Vinculado')
    bolsa_requerida = models.CharField(max_length=31, choices=BOLSA_REQUERIDA_CHOICES, verbose_name='Bolsa Requerida')
    sexo = models.CharField(max_length=1, choices=(('M', 'Masculino'), ('F', 'Feminino')))
    profissao = models.CharField(max_length=127, verbose_name='Profissão')
    tipo_documento = models.CharField(max_length=3, choices=(('RG', 'RG'), ('CNH', 'CNH')), verbose_name='Tipo de Documento')
    numero_documento = models.CharField(max_length=31, verbose_name='Número do Documento')
    orgao_expeditor = models.CharField(max_length=15, verbose_name='Órgão Expeditor')
    data_emissao = models.DateField(verbose_name='Data de Emissão')
    uf_nascimento = models.CharField(max_length=2, verbose_name='UF de Nascimento')
    municipio_nascimento = models.CharField(max_length=255, verbose_name='Município de Nascimento')
    estado_civil = models.CharField(max_length=15, choices=ESTADO_CIVIL_CHOICES, verbose_name='Estado Civil')
    nome_conjuge = models.CharField(max_length=255, null=True, blank=True, verbose_name='Nome do Cônjuge')
    nome_pai = models.CharField(max_length=255, null=True, blank=True, verbose_name='Nome do Pai')
    nome_mae = models.CharField(max_length=255, verbose_name='Nome da Mãe')
    endereco = models.ForeignKey(Endereco, on_delete=models.SET_NULL, null=True, verbose_name='Endereço')
    telefone = models.CharField(max_length=15)
    area_ultimo_curso_superior = models.CharField(max_length=10, choices=ULTIMO_CURSO_SUPERIOR_CHOICES, verbose_name='Área do Último Curso Superior')
    ultimo_curso_titulacao = models.CharField(max_length=127, verbose_name='Último Curso de Titulação')
    instituicao_titulacao = models.CharField(max_length=127, verbose_name='Instituição de Titulação')
    dados_bancarios = models.ForeignKey(DadosBancarios, on_delete=models.SET_NULL, null=True)
    data_inicio_vinculacao = models.DateField(verbose_name='Data de Início da Vinculação')
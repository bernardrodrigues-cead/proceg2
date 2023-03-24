from django import forms
from FichaUab.utils.validators import is_cpf_valid

from FichaUab.models import PessoaFichaUab

class CpfForm(forms.Form):
    cpf = forms.CharField(max_length=14, validators=[is_cpf_valid])

class PessoaFichaUabForm(forms.ModelForm):
    # Pessoa
    nome = forms.CharField(max_length=255)
    cpf = forms.CharField(max_length=14)
    data_nascimento = forms.DateField()
    email = forms.EmailField()

    # Endereço
    cep = forms.CharField(max_length=8)
    logradouro = forms.CharField(max_length=255)
    numero = forms.CharField(max_length=15)
    complemento = forms.CharField(max_length=31, required=False)
    referencia = forms.CharField(max_length=63, required=False)
    bairro = forms.CharField(max_length=127)
    cidade = forms.CharField(max_length=127)
    estado = forms.CharField(max_length=2)

    # Dados Bancários
    banco = forms.CharField(max_length=127)
    agencia = forms.CharField(max_length=31)
    conta = forms.CharField(max_length=31)
    operacao = forms.CharField(max_length=7, required=False)
    
    class Meta:
        model = PessoaFichaUab
        fields = [
            'curso_vinculado',
            'bolsa_requerida',
            'sexo',
            'profissao',
            'tipo_documento',
            'numero_documento',
            'orgao_expeditor',
            'data_emissao',
            'uf_nascimento',
            'municipio_nascimento',
            'estado_civil',
            'nome_conjuge',
            'nome_pai',
            'nome_mae',
            'telefone',
            'area_ultimo_curso_superior',
            'ultimo_curso_titulacao',
            'instituicao_titulacao',
            'data_inicio_vinculacao',
        ]
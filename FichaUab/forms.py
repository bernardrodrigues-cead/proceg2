from django import forms
from FichaUab.utils.validators import is_cpf_valid

from FichaUab.models import PessoaFichaUab

class CpfForm(forms.Form):
    cpf = forms.CharField(max_length=14, validators=[is_cpf_valid], label="CPF")

class PessoaFichaUabForm(forms.ModelForm):
    # Pessoa
    nome = forms.CharField(max_length=255)
    cpf = forms.CharField(max_length=14, label='CPF')
    data_nascimento = forms.DateField(label='Data de Nascimento')
    email = forms.EmailField(label='E-mail')

    # Endereço
    cep = forms.CharField(max_length=8, label='CEP')
    logradouro = forms.CharField(max_length=255)
    numero = forms.CharField(max_length=15, label='Número')
    complemento = forms.CharField(max_length=31, required=False)
    referencia = forms.CharField(max_length=63, required=False, label='Referência')
    bairro = forms.CharField(max_length=127)
    cidade = forms.CharField(max_length=127)
    estado = forms.CharField(max_length=2)

    # Dados Bancários
    banco = forms.CharField(max_length=127)
    agencia = forms.CharField(max_length=31, label='Agência')
    conta = forms.CharField(max_length=31)
    operacao = forms.CharField(max_length=7, required=False, label='Operação')
    
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
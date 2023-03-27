from collections import OrderedDict
from django import forms
from django.shortcuts import redirect, render
from django.views.generic.edit import UpdateView, CreateView

from FichaUab.forms import CpfForm, PessoaFichaUabForm
from FichaUab.models import DadosBancarios, Endereco, Pessoa, PessoaFichaUab

# Create your views here.
def index(request):
    if request.method == 'POST':
        # Recebe o modelo de formulário que será recebido no método post
        form = CpfForm(request.POST)
        if form.is_valid():
            # Remove os traços e pontos do CPF
            cpf = ''.join(c for c in form.cleaned_data['cpf'] if c.isdigit())
            
            # Existe a pessoa no sistema
            if Pessoa.objects.filter(cpf=cpf):
                pessoa = Pessoa.objects.get(cpf=cpf)
                
                # Existe a pessoa no sistema e ela possui ficha UAB
                if PessoaFichaUab.objects.filter(pessoa=pessoa):
                    response = redirect('update_pessoa_ficha_uab', PessoaFichaUab.objects.get(pessoa=pessoa).pk)

                # Existe a pessoa no sistema e ela não possui ficha UAB
                else:
                    response = redirect('create_pessoa_ficha_uab')

                # Armazena no cookie dados que serão utilizados na tela seguinte
                response.set_cookie('cpf', pessoa.cpf)
                response.set_cookie('nome', pessoa.nome)
                response.set_cookie('data_nascimento', pessoa.data_nascimento)
                response.set_cookie('email', pessoa.email)
                return response
            
            # Não existe a pessoa no sistema
            else:
                response = redirect('create_pessoa')
                
                # Armazena no cookie apenas o CPF
                response.set_cookie('cpf', cpf)
                return response
    
    # Armazena o formulário que será exibido no método GET
    form = CpfForm()
    return render(request, 'fichaUab/index.html', {'form': form})

class PessoaCreateView(CreateView):
    model = Pessoa
    fields = '__all__'
    template_name = 'fichaUab/create_pessoa.html'
    success_url = '/fichauab/create'
   
    # Função para reordenar os campos do formulário
    def order_fields(self, fields):
        return OrderedDict([
            ('cpf', fields['cpf']),
            ('nome', fields['nome']),
            ('data_nascimento', fields['data_nascimento']),
            ('email', fields['email']),
            ('confirmacao_email', fields['confirmacao_email'])
        ])
    
    # Função para realizar manutenções no formulário
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['confirmacao_email'] = forms.EmailField(label="Confirmação de e-mail")
        form.fields['cpf'].widget = forms.TextInput({'readonly': True})
        form.fields['data_nascimento'].widget = forms.DateInput({'type': 'date'})
        # Chamada da função de reordenação dos campos
        form.fields = self.order_fields(form.fields)
        return form
    

    # Função para preencher os campos com valores enviados pelo Cookie
    def get_initial(self):
        initial = super().get_initial()
        initial['cpf'] = self.request.COOKIES.get('cpf')
        return initial

    # Caso o formulário seja válido...
    def form_valid(self, form):
        # Armazena os campos recebidos pelo formulário
        # mas não envia para o Banco de Dados
        new_data = form.save(commit=False)
        # Remove os traços e pontos do CPF
        new_data.cpf = ''.join(c for c in form.cleaned_data['cpf'] if c.isdigit())
        # Após a correção do CPF, envia para o Banco de Dados
        new_data.save()

        # Armazena no cookie dados que serão utilizados na tela seguinte
        response = redirect('create_pessoa_ficha_uab')
        response.set_cookie('cpf', new_data.cpf)
        response.set_cookie('nome', new_data.nome)
        response.set_cookie('data_nascimento', new_data.data_nascimento)
        response.set_cookie('email', new_data.email)
        return response
    
class PessoaFichaUabCreateView(CreateView):
    form_class = PessoaFichaUabForm
    success_url = '/fichauab'
    template_name = 'fichaUab/create_pessoa_ficha_uab.html'

    # Função para preencher os campos com valores enviados pelo Cookie
    def get_initial(self):
        initial = super().get_initial()
        initial['cpf'] = self.request.COOKIES.get('cpf')
        initial['nome'] = self.request.COOKIES.get('nome')
        initial['email'] = self.request.COOKIES.get('email')
        initial['data_nascimento'] = self.request.COOKIES.get('data_nascimento')
        return initial
    
    # Função para realizar manutenções no formulário
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['cpf'].widget = forms.TextInput({'readonly': True})
        form.fields['nome'].widget = forms.TextInput({'readonly': True})
        form.fields['data_nascimento'].widget = forms.DateInput({'type': 'date', 'readonly': True})
        form.fields['data_emissao'].widget = forms.DateInput({'type': 'date'})
        form.fields['data_inicio_vinculacao'].widget = forms.DateInput({'type': 'date'})
        return form
    
    # Caso o formulário seja válido...
    def form_valid(self, form):
        # Armazena o novo Endereço
        new_endereco = Endereco(
            cep = form.cleaned_data['cep'],
            logradouro = form.cleaned_data['logradouro'],
            numero = form.cleaned_data['numero'],
            complemento = form.cleaned_data['complemento'],
            referencia = form.cleaned_data['referencia'],
            bairro = form.cleaned_data['bairro'],
            cidade = form.cleaned_data['cidade'],
            estado = form.cleaned_data['estado'],
        )
        new_endereco.save()

        # Armazena os novos Dados Bancários
        new_dados_bancarios = DadosBancarios(
            pessoa = Pessoa.objects.get(cpf=''.join(c for c in form.cleaned_data['cpf'] if c.isdigit())),
            banco = form.cleaned_data['banco'],
            agencia = form.cleaned_data['agencia'],
            conta = form.cleaned_data['conta'],
            operacao = form.cleaned_data['operacao']
        )
        new_dados_bancarios.save()

        # Armazena os campos recebidos pelo formulário
        # mas não envia para o Banco de Dados
        new_data = form.save(commit=False)
        # Salva os dados faltantes do formulário
        new_data.pessoa = Pessoa.objects.get(cpf=''.join(c for c in form.cleaned_data['cpf'] if c.isdigit()))
        new_data.endereco = new_endereco
        new_data.dados_bancarios = new_dados_bancarios

        new_data.save()
        return redirect('index')
    
class PessoaFichaUabUpdateView(UpdateView):
    form_class = PessoaFichaUabForm
    model = PessoaFichaUab
    success_url = '/fichauab'
    template_name = 'fichaUab/update_pessoa_ficha_uab.html'

    # Função para preencher os campos com valores enviados pelo Cookie
    def get_initial(self):
        initial = super().get_initial()
        # Dados de Pessoa
        initial['cpf'] = self.request.COOKIES.get('cpf')
        initial['nome'] = self.request.COOKIES.get('nome')
        initial['email'] = self.request.COOKIES.get('email')
        initial['data_nascimento'] = self.request.COOKIES.get('data_nascimento')

        # Dados de Endereço
        initial['cep'] = self.object.endereco.cep
        initial['logradouro'] = self.object.endereco.logradouro
        initial['numero'] = self.object.endereco.numero
        initial['complemento'] = self.object.endereco.complemento
        initial['referencia'] = self.object.endereco.referencia
        initial['bairro'] = self.object.endereco.bairro
        initial['cidade'] = self.object.endereco.cidade
        initial['estado'] = self.object.endereco.estado

        # Dados Bancários
        initial['banco'] = self.object.dados_bancarios.banco
        initial['agencia'] = self.object.dados_bancarios.agencia
        initial['conta'] = self.object.dados_bancarios.conta
        initial['operacao'] = self.object.dados_bancarios.operacao
        
        return initial
    
    # Função para realizar manutenções no formulário
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['cpf'].widget = forms.TextInput({'readonly': True})
        form.fields['nome'].widget = forms.TextInput({'readonly': True})
        form.fields['data_nascimento'].widget = forms.DateInput({'type': 'date', 'readonly': True})
        form.fields['data_emissao'].widget = forms.DateInput({'type': 'date'})
        form.fields['data_inicio_vinculacao'].widget = forms.DateInput({'type': 'date'})
        return form
    
    # Caso o formulário seja válido...
    def form_valid(self, form):
        # Armazena o novo Endereço
        new_endereco = Endereco(
            cep = form.cleaned_data['cep'],
            logradouro = form.cleaned_data['logradouro'],
            numero = form.cleaned_data['numero'],
            complemento = form.cleaned_data['complemento'],
            referencia = form.cleaned_data['referencia'],
            bairro = form.cleaned_data['bairro'],
            cidade = form.cleaned_data['cidade'],
            estado = form.cleaned_data['estado'],
        )
        new_endereco.save()

        # Armazena os novos Dados Bancários
        new_dados_bancarios = DadosBancarios(
            pessoa = Pessoa.objects.get(cpf=''.join(c for c in form.cleaned_data['cpf'] if c.isdigit())),
            banco = form.cleaned_data['banco'],
            agencia = form.cleaned_data['agencia'],
            conta = form.cleaned_data['conta'],
            operacao = form.cleaned_data['operacao']
        )
        new_dados_bancarios.save()

        # Armazena os campos recebidos pelo formulário
        # mas não envia para o Banco de Dados
        new_data = form.save(commit=False)
        # Salva os dados faltantes do formulário
        new_data.pessoa = Pessoa.objects.get(cpf=''.join(c for c in form.cleaned_data['cpf'] if c.isdigit()))
        new_data.endereco = new_endereco
        new_data.dados_bancarios = new_dados_bancarios

        new_data.save()
        return redirect('index')
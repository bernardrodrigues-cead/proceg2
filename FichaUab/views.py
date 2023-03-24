from django import forms
from django.shortcuts import redirect, render
from django.views.generic.edit import UpdateView, CreateView

from FichaUab.forms import CpfForm, PessoaFichaUabForm
from FichaUab.models import DadosBancarios, Endereco, Pessoa, PessoaFichaUab

# Create your views here.
def index(request):
    if request.method == 'POST':
        form = CpfForm(request.POST)
        if form.is_valid():
            cpf = ''.join(c for c in form.cleaned_data['cpf'] if c.isdigit())
            
            # Existe a pessoa no sistema
            if Pessoa.objects.filter(cpf=cpf):
                pessoa = Pessoa.objects.get(cpf=cpf)
                
                # Existe a pessoa no sistema e ela possui ficha UAB
                if PessoaFichaUab.objects.filter(pessoa=pessoa):
                    response = redirect('update_pessoa_ficha_uab')

                # Existe a pessoa no sistema e ela não possui ficha UAB
                else:
                    response = redirect('create_pessoa_ficha_uab')

                response.set_cookie('cpf', pessoa.cpf)
                response.set_cookie('nome', pessoa.nome)
                response.set_cookie('data_nascimento', pessoa.data_nascimento)
                response.set_cookie('email', pessoa.email)
                return response
            
            # Não existe a pessoa no sistema
            else:
                response = redirect('create_pessoa')
                response.set_cookie('cpf', cpf)
                return response
    
    form = CpfForm()
    return render(request, 'fichaUab/index.html', {'form': form})

class PessoaCreateView(CreateView):
    model = Pessoa
    fields = '__all__'
    template_name = 'fichaUab/create_pessoa.html'
    success_url = '/fichauab'
   
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['cpf'].widget = forms.TextInput({'disabled': True})
        form.fields['data_nascimento'].widget = forms.DateInput({'type': 'date'})
        return form

    def get_initial(self):
        initial = super().get_initial()
        initial['cpf'] = self.request.COOKIES.get('cpf')
        return initial

    def form_valid(self, form):
        new_data = form.save(commit=False)
        new_data.cpf = ''.join(c for c in form.cleaned_data['cpf'] if c.isdigit())
        new_data.save()
        return super().form_valid(form)
    
class PessoaFichaUabCreateView(CreateView):
    form_class = PessoaFichaUabForm
    success_url = '/fichauab'
    template_name = 'fichaUab/create_pessoa_ficha_uab.html'

    def get_initial(self):
        initial = super().get_initial()
        initial['cpf'] = self.request.COOKIES.get('cpf')
        initial['nome'] = self.request.COOKIES.get('nome')
        initial['email'] = self.request.COOKIES.get('email')
        initial['data_nascimento'] = self.request.COOKIES.get('data_nascimento')
        return initial
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['cpf'].widget = forms.TextInput({'disabled': True})
        form.fields['nome'].widget = forms.TextInput({'disabled': True})
        form.fields['data_nascimento'].widget = forms.DateInput({'type': 'date', 'disabled': True})
        return form
    
    def form_valid(self, form):
        new_endereco = Endereco(
            cep = forms.cleaned_data['cep'],
            logradouro = forms.cleaned_data['logradouro'],
            numero = forms.cleaned_data['numero'],
            complemento = forms.cleaned_data['complemento'],
            referencia = forms.cleaned_data['referencia'],
            bairro = forms.cleaned_data['bairro'],
            cidade = forms.cleaned_data['cidade'],
            estado = forms.cleaned_data['estado'],
        )
        new_endereco.save()

        new_dados_bancarios = DadosBancarios(
            pessoa = Pessoa.objects.get(cpf=forms.cleaned_data['cpf']),
            banco = forms.cleaned_data['banco'],
            agencia = forms.cleaned_data['agencia'],
            conta = forms.cleaned_data['conta'],
            operacao = forms.cleaned_data['operacao']
        )
        new_dados_bancarios.save()

        new_data = form.save(commit=False)
        new_data.pessoa = Pessoa.objects.get(cpf=form.cleaned_data['cpf'])
        new_data.endereco = new_endereco
        new_data.dados_bancarios = new_dados_bancarios

        new_data.save()
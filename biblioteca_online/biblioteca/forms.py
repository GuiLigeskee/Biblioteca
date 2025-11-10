from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Livro, Emprestimo, Reserva, PerfilUsuario
from datetime import timedelta
from django.utils import timezone


class RegistroUsuarioForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, label='Nome')
    last_name = forms.CharField(max_length=30, required=True, label='Sobrenome')
    email = forms.EmailField(required=True, label='Email')
    
    # Campos do perfil
    cpf = forms.CharField(max_length=14, required=True, label='CPF', 
                         widget=forms.TextInput(attrs={'placeholder': 'XXX.XXX.XXX-XX'}))
    data_nascimento = forms.DateField(required=True, label='Data de Nascimento',
                                     widget=forms.DateInput(attrs={'type': 'date'}))
    telefone = forms.CharField(max_length=20, required=True, label='Telefone',
                              widget=forms.TextInput(attrs={'placeholder': '(XX) XXXXX-XXXX'}))
    endereco = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), 
                              required=True, label='Endereço')

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

    def clean_cpf(self):
        cpf = self.cleaned_data.get('cpf')
        # Verificar se o CPF já existe
        if PerfilUsuario.objects.filter(cpf=cpf).exists():
            raise forms.ValidationError('Este CPF já está cadastrado no sistema.')
        return cpf
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        # Verificar se o email já existe
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Este email já está cadastrado no sistema.')
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        
        if commit:
            user.save()
            # Criar perfil do usuário
            PerfilUsuario.objects.create(
                user=user,
                cpf=self.cleaned_data['cpf'],
                data_nascimento=self.cleaned_data['data_nascimento'],
                telefone=self.cleaned_data['telefone'],
                endereco=self.cleaned_data['endereco']
            )
        return user


class LivroForm(forms.ModelForm):
    class Meta:
        model = Livro
        fields = ['titulo', 'autor', 'editora', 'ano_publicacao', 'genero', 
                 'isbn', 'quantidade_total', 'quantidade_disponivel']
        labels = {
            'titulo': 'Título',
            'autor': 'Autor',
            'editora': 'Editora',
            'ano_publicacao': 'Ano de Publicação',
            'genero': 'Gênero',
            'isbn': 'ISBN',
            'quantidade_total': 'Quantidade Total',
            'quantidade_disponivel': 'Quantidade Disponível'
        }
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'autor': forms.TextInput(attrs={'class': 'form-control'}),
            'editora': forms.TextInput(attrs={'class': 'form-control'}),
            'ano_publicacao': forms.NumberInput(attrs={'class': 'form-control'}),
            'genero': forms.TextInput(attrs={'class': 'form-control'}),
            'isbn': forms.TextInput(attrs={'class': 'form-control'}),
            'quantidade_total': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
            'quantidade_disponivel': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
        }


class EmprestimoForm(forms.ModelForm):
    dias_emprestimo = forms.IntegerField(
        min_value=1, 
        max_value=30, 
        initial=7,
        label='Dias de Empréstimo',
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Emprestimo
        fields = ['livro', 'usuario']
        labels = {
            'livro': 'Livro',
            'usuario': 'Usuário'
        }
        widgets = {
            'livro': forms.Select(attrs={'class': 'form-control'}),
            'usuario': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Apenas livros com quantidade disponível
        self.fields['livro'].queryset = Livro.objects.filter(quantidade_disponivel__gt=0)

    def save(self, commit=True):
        emprestimo = super().save(commit=False)
        dias = self.cleaned_data['dias_emprestimo']
        emprestimo.data_devolucao_prevista = timezone.now() + timedelta(days=dias)
        
        if commit:
            emprestimo.save()
            # Diminuir quantidade disponível
            livro = emprestimo.livro
            livro.quantidade_disponivel -= 1
            livro.save()
        return emprestimo


class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ['livro', 'usuario']
        labels = {
            'livro': 'Livro',
            'usuario': 'Usuário'
        }
        widgets = {
            'livro': forms.Select(attrs={'class': 'form-control'}),
            'usuario': forms.Select(attrs={'class': 'form-control'}),
        }


class PerfilUsuarioForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=True, label='Nome')
    last_name = forms.CharField(max_length=30, required=True, label='Sobrenome')
    email = forms.EmailField(required=True, label='Email')

    class Meta:
        model = PerfilUsuario
        fields = ['cpf', 'data_nascimento', 'telefone', 'endereco']
        labels = {
            'cpf': 'CPF',
            'data_nascimento': 'Data de Nascimento',
            'telefone': 'Telefone',
            'endereco': 'Endereço'
        }
        widgets = {
            'cpf': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'XXX.XXX.XXX-XX'}),
            'data_nascimento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '(XX) XXXXX-XXXX'}),
            'endereco': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['first_name'].initial = user.first_name
            self.fields['last_name'].initial = user.last_name
            self.fields['email'].initial = user.email

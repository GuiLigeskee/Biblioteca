# 📚 Sistema de Gerenciamento de Biblioteca

Um sistema desenvolvido em **Django** para gerenciar empréstimos, reservas, controle de atrasos e multas de livros em uma biblioteca.

## � Requisitos do Sistema Atendidos

### 1. Usuário

- ✅ **id_usuario** (PK) - identificador único
- ✅ **nome** - texto
- ✅ **cpf** - texto (formato XXX.XXX.XXX-XX)
- ✅ **data_nascimento** - data
- ✅ **telefone** - texto
- ✅ **email** - texto
- ✅ **senha** - texto (hash)
- ✅ **endereço** - texto

### 2. Admin

- ✅ **id_admin** (PK) - inteiro
- ✅ **nome** - texto
- ✅ **email** - texto
- ✅ **senha** - texto (hash)
- ✅ **nivel_acesso** - inteiro (ex.: 1=geral, 2=superadmin)

### 3. Livro

- ✅ **id_livro** (PK) - inteiro
- ✅ **titulo** - texto
- ✅ **autor** - texto
- ✅ **editora** - texto
- ✅ **ano_publicacao** - inteiro
- ✅ **genero** - texto
- ✅ **isbn** - texto
- ✅ **quantidade_total** - inteiro
- ✅ **quantidade_disponivel** - inteiro

### 4. Reserva

- ✅ **id_reserva** (PK) - inteiro
- ✅ **id_usuario** (FK) - referência a Usuário
- ✅ **id_livro** (FK) - referência a Livro
- ✅ **data_reserva** - data/hora
- ✅ **status** - texto (ex.: ativa, concluída, cancelada)

### 5. Empréstimo

- ✅ **id_emprestimo** (PK) - inteiro
- ✅ **id_usuario** (FK) - referência a Usuário
- ✅ **id_livro** (FK) - referência a Livro
- ✅ **data_emprestimo** - data/hora
- ✅ **data_devolucao_prevista** - data/hora
- ✅ **data_devolucao_real** - data/hora (pode ser nulo)
- ✅ **multa** - decimal (valor monetário, se houver atraso)

## 📝 Funcionalidades

- **Cadastro de Livros**: Gerenciamento completo do acervo com controle de quantidade.
- **Empréstimos**: Controle de empréstimos com cálculo automático de multas por atraso.
- **Reservas**: Sistema de reservas com controle de status.
- **Controle de Atrasos e Multas**: Cálculo automático de multas (R$ 1,00 por dia de atraso).
- **Área do Usuário**:
  - Visualizar empréstimos ativos.
  - Gerenciar reservas realizadas.
  - Perfil com dados pessoais (CPF, telefone, endereço).
- **Administração**:
  - Marcar devoluções com cálculo automático de multas.
  - Gerenciar o acervo de livros.
  - Controle de níveis de acesso.

## 🛠️ Tecnologias Utilizadas

- **Backend**: Django 5.2+
- **Banco de Dados**: SQLite (desenvolvimento) / PostgreSQL (produção)
- **Frontend**: Django Templates, Bootstrap 5
- **Autenticação**: Sistema nativo do Django
- **Deploy**: Gunicorn, WhiteNoise

## 🚀 Como Iniciar o Projeto (Desenvolvimento)

### 1. Clone o repositório

```bash
git clone https://github.com/GuiLigeskee/Biblioteca.git
cd Biblioteca
```

### 2. Crie e ative um ambiente virtual

```powershell
python -m venv .venv
.venv\Scripts\Activate
```

### 3. Instale as dependências

```powershell
pip install -r requirements.txt
```

### 4. Execute as migrações

```powershell
cd biblioteca_online
python manage.py migrate
```

### 5. Crie um superusuário (administrador)

```powershell
python manage.py createsuperuser
```

### 6. Inicie o servidor de desenvolvimento

```powershell
python manage.py runserver
```

### 7. Acesse o sistema

- **Site**: http://127.0.0.1:8000/
- **Painel Administrativo**: http://127.0.0.1:8000/admin/

## 🌐 Como Fazer Deploy (Produção)

### Opção Rápida: Railway (Recomendado)

1. **Leia o guia completo**: [DEPLOY_RAPIDO.md](DEPLOY_RAPIDO.md)
2. **Execute a verificação**: `python check_deploy.py`
3. **Siga os 3 passos** no guia rápido

### Outras Plataformas

- **Heroku**: Guia completo em [DEPLOY.md](DEPLOY.md)
- **Render**: Deploy gratuito com limitações
- **Docker**: Configuração incluída

📚 **Documentação de Deploy**:

- [DEPLOY_RAPIDO.md](DEPLOY_RAPIDO.md) - Deploy em 3 passos
- [DEPLOY.md](DEPLOY.md) - Guia completo com todas as opções
- [COMANDOS_UTEIS.md](COMANDOS_UTEIS.md) - Referência de comandos

## 📦 Estrutura do Projeto

```
Biblioteca/
├── biblioteca_online/
│   ├── biblioteca/          # App principal
│   │   ├── models.py       # Modelos (Livro, Empréstimo, Reserva, etc.)
│   │   ├── views.py        # Views
│   │   ├── urls.py         # URLs
│   │   ├── admin.py        # Configuração do admin
│   │   └── migrations/     # Migrações do banco
│   ├── biblioteca_online/  # Configurações do projeto
│   │   ├── settings.py
│   │   └── urls.py
│   ├── templates/          # Templates HTML
│   ├── static/             # Arquivos estáticos
│   ├── db.sqlite3          # Banco de dados
│   └── manage.py           # Script de gerenciamento
├── requirements.txt        # Dependências
└── README.md
```

## 👤 Autor

**Guilherme Ligeski**

- GitHub: [@GuiLigeskee](https://github.com/GuiLigeskee)

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

# 📚 Sistema de Gerenciamento de Biblioteca

Um sistema desenvolvido em **Django** para gerenciar empréstimos, reservas, controle de atrasos e multas de livros em uma biblioteca.

## 📝 Funcionalidades

- **Cadastro de Livros**: Gerenciamento de acervo, incluindo título, autor e disponibilidade.
- **Empréstimos**: Usuários podem emprestar livros disponíveis, com controle automático de devolução.
- **Reservas**: Quando um livro está indisponível, é possível realizar reservas e entrar em uma fila de espera.
- **Controle de Atrasos e Multas**: Cálculo automático de multas para empréstimos atrasados.
- **Área do Usuário**:
  - Visualizar empréstimos ativos.
  - Gerenciar reservas realizadas.
- **Administração**:
  - Marcar devoluções.
  - Gerenciar o acervo de livros.

## 🛠️ Tecnologias Utilizadas

- **Backend**: Django 5.1.3
- **Banco de Dados**: SQLite
- **Frontend**: Django Templates, Bootstrap
- **Autenticação**: Sistema nativo do Django


# Rotas Disponíveis no Sistema de Biblioteca

## 📚 Rotas Públicas (Qualquer pessoa)

- **/** → Catálogo de livros (lista_livros)
- **/livros/{id}/** → Detalhes de um livro específico
- **/registro/** → Cadastro de novo usuário
- **/login/** → Login no sistema
- **/logout/** → Logout (POST apenas)

## 👤 Rotas de Usuário Autenticado

### Empréstimos

- **/livros/{id}/emprestar/** → Solicitar empréstimo de um livro
- **/meus-emprestimos/** → Ver meus empréstimos
- **/emprestimos/{id}/devolver/** → Devolver um livro

### Reservas

- **/livros/{id}/reservar/** → Fazer reserva de um livro
- **/minhas-reservas/** → Ver minhas reservas
- **/reservas/{id}/cancelar/** → Cancelar uma reserva

### Perfil

- **/perfil/** → Editar meu perfil

## 🔧 Rotas Administrativas (Apenas Staff)

### Gerenciar Livros

- **/admin/livros/cadastrar/** → Cadastrar novo livro
- **/admin/livros/{id}/editar/** → Editar um livro existente

### Gerenciar Empréstimos

- **/admin/emprestimos/** → Listar todos os empréstimos
- **/admin/emprestimos/criar/** → Criar empréstimo manualmente
- **/admin/emprestimos/{id}/devolver/** → Marcar empréstimo como devolvido

### Gerenciar Reservas

- **/admin/reservas/** → Listar todas as reservas

### Painel Django Admin

- **/admin/** → Painel administrativo completo do Django

## ⚠️ Erros Comuns

### Page not found (404)

Se você está vendo erro 404, verifique:

1. **URL digitada corretamente?**

   - ✅ `/admin/livros/cadastrar/`
   - ❌ `/admin/livros/cadastrar` (falta a barra final)

2. **Você tem permissão?**

   - Rotas `/admin/*` exigem que você seja **staff**
   - Para tornar um usuário staff: vá em `/admin/` → Auth → Users → edite o usuário → marque "Staff status"

3. **O servidor está rodando?**
   - Execute: `python biblioteca_online/manage.py runserver`

### Method Not Allowed (405)

- O logout agora exige POST, não GET
- Use o botão "Sair" no menu, não digite `/logout/` diretamente

### Integrity Error (Registro)

- CPF ou email já existe no sistema
- Use CPF e email diferentes

## 🚀 Como Acessar as Rotas Administrativas

1. **Faça login** com um usuário staff
2. **Clique no menu "Administração"** no topo
3. **Escolha a opção desejada**:
   - Cadastrar Livro
   - Gerenciar Empréstimos
   - Gerenciar Reservas
   - Painel Admin Django

## 💡 Dica

Para transformar seu usuário em staff:

1. Acesse `/admin/`
2. Login com superusuário (criado com `createsuperuser`)
3. Vá em **Authentication and Authorization** → **Users**
4. Edite o usuário desejado
5. Marque ✅ **Staff status**
6. Salve

Agora esse usuário pode acessar todas as rotas `/admin/*`!

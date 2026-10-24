# 📔 Diário do Programador — Autorização de Usuário

Continuação do projeto do Diário do Programador. Hoje o diário deixa de ser de um usuário só: cada pessoa vai poder **se cadastrar**, **fazer login** e ver **apenas os próprios cartões**.

---

## ✅ O que você precisa ter instalado

1. **Python 3** — [baixe aqui](https://www.python.org/downloads/) se ainda não tiver.
   - Para conferir se já tem, abra o terminal e digite:
     ```bash
     python --version
     ```
2. **Flask** e **Flask-SQLAlchemy**.

---

## 🚀 Passo a passo para rodar o projeto

**1. Baixe o projeto** e entre na pasta dele pelo terminal.

**2. Instale as bibliotecas necessárias**
```bash
pip install flask
pip install Flask-SQLAlchemy
```

**3. Crie o banco de dados**

Depois de completar a **Tarefa 1** (criar a tabela `User`), rode isso no terminal, dentro da pasta do projeto:

```
python
```
```python
>>> from main import app, db
>>> app.app_context().push()
>>> db.create_all()
```

> ⚠️ Se você já tinha um `diary.db` de uma aula anterior, apague o arquivo dentro de `instance/` e repita esse passo para recriá-lo com a tabela nova.



**4. Abra `http://127.0.0.1:5000` no navegador.**

---

## 🧭 Estrutura do projeto

```
diario-do-programador/
├── main.py                → rotas, conexão com o banco, classes Card e User
├── instance/diary.db       → banco de dados (criado por você, veja o Passo 3)
├── templates/
│   ├── login.html
│   ├── registration.html
│   ├── index.html
│   ├── card.html
│   └── create_card.html
└── static/
```

---

## 🖱️ Como funciona

1. `/` → login. Se bater com um usuário cadastrado, entra e vai para `/index`.
2. `/reg` → cadastro de usuário.
3. `/index` → lista os cartões do usuário logado.
4. `/card/<id>` → mostra um cartão específico.
5. `/create` e `/form_create` → criam um cartão em nome do usuário logado.

---

## 📝 Atividades — o que precisa ser feito

O arquivo `main.py` já tem **comentários** em cada lugar que falta completar, explicando o que aquela parte precisa fazer. A ideia aqui não é te dar a resposta pronta, mas mostrar o **padrão** que você precisa seguir — você ainda precisa adaptar para cada caso. Siga a ordem abaixo, ela segue o fluxo do site.

### Tarefa 1 — Criar a classe `User`
📄 Local: `main.py`, logo abaixo da classe `Card`

```python
class User(db.Model):
    #LEMBRE COMO CRIAMOS O BANCO DE DADOS ACIMA, TODOS SERÃO COLUNAS, MAS DE TIPOS DIFERENTES
    
    #id = 
    #email = 
    #password =
```
A classe `Card`, logo acima no arquivo, já tem o padrão de como declarar uma coluna:
```python
id = db.Column(db.Integer, primary_key=True)
title = db.Column(db.String(100), nullable=False)
```
O `id` do `User` segue exatamente essa mesma lógica (número inteiro, chave primária):
```python
id = db.Column(db.Integer, primary_key=True)
```
Para `email` e `password`, use `db.String(tamanho)` — um texto curto, com um limite de caracteres que você escolhe (por exemplo, 100 para o e-mail, 30 para a senha) — e não esqueça do `nullable=False` em cada um, para que nenhum usuário seja salvo sem e-mail ou sem senha.

### Tarefa 3 — Salvar o usuário no banco (rota `/reg`)
📄 Local: `main.py`, na função `reg`

```python
# TAREFA 3. Salvar usuário no banco
#DENTRO DO USUÁRIO PRECISAMOS DE EMAIL E SENHA, QUE JÁ FORAM CRIADOS LOGO ACIMA COMO EMAIL E PASSWORD
#user =

#AGORA PRECISAMOS ADICIONAR O USUÁRIO AO BANCO DE DADOS E COMMITAR, UTILIZE db.session.add(variável) E db.session.commit() PARA ISSO
```
O padrão para criar um registro é o mesmo que você já usou para criar um `Card` lá embaixo no arquivo:
```python
Card(coluna1=valor1, coluna2=valor2)
```
Troque `Card` por `User`, e as colunas pelas que você criou na Tarefa 1. Os valores já estão prontos nas variáveis `email` e `password`, logo acima desse comentário — então fica assim:
```python
user = User(email=email, password=password)
```
Depois é só salvar, com o mesmo par de comandos que você já usa para o `Card`:
```python
db.session.add(user)
db.session.commit()
```

### Tarefa 4 — Verificação do login (rota `/`)
📄 Local: `main.py`, na função `login`

```python
# TAREFA 4. Verificação do usuário
#Aqui precisamos buscar todos os usuarios no banco utilizando User.query.all() 
    #users_db = 

#Aqui criaremos a condição de login, onde form_login e password serão comparados com os dados do banco de dados, e caso sejam iguais, o usuário será redirecionado para a página de conteúdo
    #for user in users_db:
       
#Aqui teremos o erro caso o usuário não seja encontrado, e será exibido na tela de login
    #error =
    #return
```
São três partes:
1. Buscar todos os usuários:
   ```python
   users_db = User.query.all()
   ```
2. Percorrer esses usuários comparando com o que foi digitado:
   ```python
   for user in users_db:
       if form_login == user.email and form_password == user.password:
           session['user_email'] = user.email
           return redirect('/index')
   ```
   O `session` é o recurso do Flask (importado lá no topo do arquivo) que guarda essa informação entre uma página e outra — é por isso que ele aparece de novo nas Tarefas 4.2 e 4.3, para "lembrar" quem está logado.
3. Se o `for` terminar e ninguém bateu, a função precisa mostrar o erro e reexibir a página de login:
   ```python
   error = 'Usuário ou senha incorretos'
   return render_template('login.html', error=error)
   ```

### Tarefa 4.2 — Criar o card em nome do usuário logado (rota `/form_create`)
📄 Local: `main.py`, na função `form_create`

```python
# TAREFA 4.2 Criar card em nome do usuário logado
#O email será igual ao email da session
#email = 

#Precisamos adicionar o email do usuário logado ao card, para isso, precisamos adicionar o campo user_email ao card, e o valor será o email da session
card = Card(title=title, subtitle=subtitle, text=text)
```
Pegue o e-mail de quem está logado a partir do `session`, o mesmo recurso usado na Tarefa 4:
```python
email = session['user_email']
```
E adicione um argumento a mais na criação do `card`, usando o campo `user_email` que já existe na classe `Card`:
```python
card = Card(title=title, subtitle=subtitle, text=text, user_email=email)
```

### Tarefa 4.3 — Mostrar só os cards do usuário logado (rota `/index`)
📄 Local: `main.py`, na função `index`

```python
# TAREFA 4.3 Mostrar apenas os cards do usuário logado
#O email será igual ao email da session
#email =

#Não será order_by, mas sim filter_by, para filtrar apenas os cards do usuário logado
cards = Card.query.order_by(Card.id).all()
```
Essa linha hoje traz os cards de **todo mundo**. Pegue o e-mail da sessão, igual na Tarefa 4.2:
```python
email = session['user_email']
```
E troque o `.order_by(Card.id)` por um `filter_by`, filtrando pelo `user_email`, mantendo a ordenação por `id`:
```python
cards = Card.query.filter_by(user_email=email).order_by(Card.id).all()
```

> 💡 Repare que as Tarefas 4, 4.2 e 4.3 sempre voltam ao mesmo lugar: "quem está logado agora?". Depois que você resolver isso uma vez (na Tarefa 4), é só reaproveitar nas outras duas.

---

## 🛠️ Problemas comuns

| Problema | Possível solução |
|---|---|
| `ModuleNotFoundError: No module named 'flask_sqlalchemy'` | `pip install Flask-SQLAlchemy` de novo, na pasta certa | 
Caso o erro persista ao criar o banco de dados tenha certeza de ter apenas uma versão do python instalado | Utilize `python -3.13`
| Tabela `user` não encontrada | Apague `instance/diary.db` e repita o Passo 3 depois de criar a classe `User` |
| Login não redireciona nem mostra erro | Confira se todos os caminhos da função `login` terminam em algum `return` |
| `/index` mostra cards de outras contas | A Tarefa 4.3 ainda não está filtrando corretamente |
| Card criado não aparece na sua lista | Confira se a Tarefa 4.2 está salvando o dono certo no card |

---

## 📚 Aprendizados desse projeto

- Criar uma segunda tabela relacionada à primeira
- Usar sessão para lembrar quem está logado
- Comparar dados de um formulário com registros do banco
- Filtrar registros de uma tabela por uma condição

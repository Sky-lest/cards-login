# Importar
from flask import Flask, render_template, request, redirect, session
# Importando a biblioteca de banco de dados

#ANTES DE UTILIZAR UTILIZE O COMANDO: pip install Flask-SQLAlchemy
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
# Definindo a chave secreta para a sessão
app.secret_key = 'my_top_secret_123'
# Conectando ao SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///diary.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Criando um Banco de Dados (DB)
db = SQLAlchemy(app)


class Card(db.Model):
    # Criando campos
    # id = coluna do banco de dados(inteiro, chave primária)
    id = db.Column(db.Integer, primary_key=True)
    # Titulo = coluna do banco de dados(string com limite de 100 caracteres, não nula)
    title = db.Column(db.String(100), nullable=False)
    # Descrição = coluna do banco de dados(string com limite de 300 caracteres, não nula)
    subtitle = db.Column(db.String(300), nullable=False)
    # Texto = coluna do banco de dados(texto, não nula)
    text = db.Column(db.Text(), nullable=False)
    # E-mail do dono do card
    user_email = db.Column(db.String(100), nullable=False)

    # Mostrando o Objeto e o ID
    def __repr__(self):
        return f'<Card {self.id}>'

# TAREFA 1. Criar uma classe USER para o banco de dados #####################################################################

class User(db.Model):
    #LEMBRE COMO CRIAMOS O BANCO DE DADOS ACIMA, TODOS SERÃO COLUNAS, MAS DE TIPOS DIFERENTES
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(30), nullable=False)

#####################################################################


# Iniciando página de login
@app.route('/', methods=['GET', 'POST'])
def login():
    error = ''

    if request.method == 'POST':
        form_login = request.form['email']
        form_password = request.form['password']

# TAREFA 4. Verificação do usuário #####################################################################
    #Aqui precisamos buscar todos os usuarios no banco utilizando User.query.all() 
        users_db = User.query.all()

    #Aqui criaremos a condição de login, onde form_login e password serão comparados com os dados do banco de dados, e caso sejam iguais, o usuário será redirecionado para a página de conteúdo
        for user in users_db:
            if form_login == user.email and form_password == user.password:
                session['user_email'] = user.email
                return redirect('/index')

    #Aqui teremos o erro caso o usuário não seja encontrado, e será exibido na tela de login
        error = 'Usuário ou senha incorretos'
        return render_template('login.html', error=error)
    
    else:
        return render_template('login.html')
#############################################################################################################

@app.route('/reg', methods=['GET', 'POST'])
def reg():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

# TAREFA 3. Salvar usuário no banco #####################################################################
        #DENTRO DO USUÁRIO PRECISAMOS DE EMAIL E SENHA, QUE JÁ FORAM CRIADOS LOGO ACIMA COMO EMAIL E PASSWORD
        user = User(email=email, password=password)
        db.session.add(user)
        db.session.commit()

        #AGORA PRECISAMOS ADICIONAR O USUÁRIO AO BANCO DE DADOS E COMMITAR, UTILIZE db.session.add(variável) E db.session.commit() PARA ISSO

        
        return redirect('/')

    return render_template('registration.html')

#############################################################################################################

# Iniciando a página de conteúdo
@app.route('/index')
def index():

# TAREFA 4.3 Mostrar apenas os cards do usuário logado ###################################################
    #O email será igual ao email da session
    email = session['user_email']
    
    #Não será order_by, mas sim filter_by, para filtrar apenas os cards do usuário logado
    cards = Card.query.filter_by(user_email=email).order_by(Card.id).all()

    return render_template('index.html',
                           cards=cards
                           )

#############################################################################################################

# Executando a página com o cartão
@app.route('/card/<int:id>')
def card(id):

    card = Card.query.get(id)

    return render_template('card.html', card=card)


# Executando a página e criando o cartão
@app.route('/create')
def create():
    return render_template('create_card.html')

# O formulário do cartão
@app.route('/form_create', methods=['GET', 'POST'])
def form_create():
    if request.method == 'POST':
        title = request.form['title']
        subtitle = request.form['subtitle']
        text = request.form['text']

############################################################################################################


# TAREFA 4.2 Criar card em nome do usuário logado
        #O email será igual ao email da session
        email = session['user_email']
        
        #Precisamos adicionar o email do usuário logado ao card, para isso, precisamos adicionar o campo user_email ao card, e o valor será o email da session
        card = Card(title=title, subtitle=subtitle, text=text, user_email=email)
        db.session.add(card)
        db.session.commit()

############################################################################################################
        return redirect('/index')
    else:
        return render_template('create_card.html')


if __name__ == "__main__":
    app.run(debug=True)
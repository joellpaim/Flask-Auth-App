# auth.py

from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from .models import User
from . import db

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return render_template('login.html')

@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()

    # Checa se o usuário já existe
    # Pega a senha fornecida pelo usuário, faz um hash e compara-o com a senha com hash no banco de dados
    if not user or not check_password_hash(user.password, password): 
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login')) # Se o usuário não existe ou a senha está incorreta, recarrega a página

    # Se a verificação acima for aprovada, saberemos que o usuário tem as credenciais corretas
    login_user(user, remember=remember)
    return redirect(url_for('main.profile'))

@auth.route('/signup')
def signup():
    return render_template('signup.html')

@auth.route('/signup', methods=['POST'])
def signup_post():

    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')

    user = User.query.filter_by(email=email).first() # Se isso retornar um usuário, o email já existe no banco de dados

    if user: # Se um usuário for encontrado, queremos redirecionar de volta para a página de inscrição para que o usuário possa tentar novamente 
        flash('Email address already exists')
        return redirect(url_for('auth.signup'))

    # Crie um novo usuário com os dados do formulário. Faça hash da senha para que a versão em texto simples não seja salva.
    new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'))

    # Adiciona o novo usuário ao banco de dados
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('auth.login'))

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))
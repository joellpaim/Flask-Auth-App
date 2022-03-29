# init.py
# https://www.digitalocean.com/community/tutorials/how-to-add-authentication-to-your-app-with-flask-login-pt#pre-requisitos

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager 

# inicia o SQLAlchemy para que possamos usá-lo posteriormente em nossos modelos
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = '9OLWxND4o83j4K4iuopO'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        # Como o user_id é apenas a chave primária da nossa tabela de usuários, use-o na consulta para o usuário
        return User.query.get(int(user_id))

    # blueprint para rotas de autenticação em nosso aplicativo
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint para partes sem autenticação do aplicativo
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
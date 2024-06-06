from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
from flask_bcrypt import Bcrypt
from app.auth import auth_bp

app = Flask(__name__)
app.config.from_object(Config)  # configuracoes do config

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)  # add bcrypt para hashear senhas

with app.app_context():
    db.create_all()

app.register_blueprint(auth_bp, url_prefix='/')

# importar as rotas após criar o app e o db
from app import routes

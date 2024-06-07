from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from instance.config import Config
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager

app = Flask(__name__)
app.config.from_object(Config)  # configuracoes do config

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)  # add bcrypt para hashear senhas
jwt = JWTManager(app)

with app.app_context():
    db.create_all()

# Importar blueprints
from app.auth import auth_bp
# importar as rotas após criar o app e o db
from app.routes import routes_bp

app.register_blueprint(auth_bp, url_prefix='/')
app.register_blueprint(routes_bp, url_prefix='/')

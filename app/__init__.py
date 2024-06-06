from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

app = Flask(__name__)
app.config.from_object(Config)  # configuracoes do config
db = SQLAlchemy(app)

# importar as rotas após criar o app e o db
from app import routes
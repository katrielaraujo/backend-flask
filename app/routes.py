from flask import jsonify
from app import app
from app.auth import register, login

@app.route('/')
def index():
    return jsonify({"message": "Bem-vindo à API de venda!"})

@app.route('/protected', methods=['GET'])
def protected():
    return jsonify({"message": "Você acessou uma rota protegida"})

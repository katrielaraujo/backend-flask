from flask import jsonify
from app import app


@app.route('/')
def index():
    return jsonify({"message": "Bem-vindo à API de venda!"})

import jwt
from flask import Blueprint, request, jsonify
from app import db, bcrypt
from app.models import Usuario
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
import datetime

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email')
    senha = data.get('senha')

    if Usuario.query.filter_by(email=email).first():
        return jsonify({"message": "Usuário já registrado."}), 400

    hashed_senha = bcrypt.generate_password_hash(senha).decode('utf-8')
    novo_usuario = Usuario(email=email, senha=hashed_senha)
    db.session.add(novo_usuario)
    db.session.commit()

    return jsonify({"message": "Usuário registrado com sucesso."}), 201


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    senha = data.get('senha')

    usuario = Usuario.query.filter_by(email=email).first()

    if not usuario or not usuario.verificar_senha(senha):
        return jsonify({"message": "Credenciais inválidas."}), 401

    access_token = create_access_token(identity=usuario.id, expires_delta=datetime.timedelta(days=1))
    return jsonify(access_token=access_token), 200

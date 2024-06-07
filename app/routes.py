from flask import Blueprint, request, jsonify
from app import db
from app.models import Venda
from flask_jwt_extended import jwt_required, get_jwt_identity

routes_bp = Blueprint('routes', __name__)


@routes_bp.route('/')
def index():
    return jsonify({"message": "Bem-vindo à API de venda!"})


@routes_bp.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    return jsonify({"message": "Você acessou uma rota protegida."})


@routes_bp.route('/sales', methods=['GET'])
@jwt_required()
def get_sales():
    vendas = Venda.query.all()
    sales_list = [
        {
            "id": venda.id,
            "nome_cliente": venda.name_cliente,
            "produto": venda.produto,
            "valor": venda.valor,
            "data_venda": venda.data_venda.strftime('%Y-%m-%d'),
            "user_id": venda.user_id
        } for venda in vendas
    ]
    return jsonify(sales_list), 200

@routes_bp.route('/sales', methods=['POST'])
@jwt_required()
def add_sale():
    data = request.get_json()
    current_user_id = get_jwt_identity()
    nova_senha = Venda(
        name_cliente = data.get('nome_cliente'),
        produto = data.get('produto'),
        valor = data.get('valor'),
        data_venda = data.get('data_venda'),
        user_id = current_user_id
    )
    db.session.add(nova_senha)
    db.session.commit()
    return jsonify({"message": "Venda adicionada com sucesso."}), 201


@routes_bp.route('/sales/<int:id>', methods=['PUT'])
@jwt_required()
def edit_sale(id):
    data = request.get_json()
    venda = Venda.query.get_or_404(id)
    if venda.user_id != get_jwt_identity():
        return jsonify({"message": "Você não tem permissão para editar esta venda."}), 403

    venda.name_cliente = data.get('nome_cliente', venda.name_cliente)
    venda.produto = data.get('produto', venda.produto)
    venda.valor = data.get('valor', venda.valor)
    venda.data_venda = data.get('data_venda', venda.data_venda)
    db.session.commit()
    return jsonify({"message": "Venda atualizada com sucesso."}), 200


@routes_bp.route('/sales/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_sale(id):
    venda = Venda.query.get_or_404(id)
    if venda.user_id != get_jwt_identity():
        return jsonify({"message": "Você não tem permissão para deletar esta venda."}), 403

    db.session.delete(venda)
    db.session.commit()
    return jsonify({"message": "Venda deletada com sucesso."}), 200

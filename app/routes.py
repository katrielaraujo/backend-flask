from flask import Blueprint, request, jsonify, send_file
from app import db
from app.models import Venda
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.utils import generate_sales_pdf
from datetime import datetime

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

    nova_vemda = Venda(
        name_cliente=data.get('nome_cliente'),
        produto=data.get('produto'),
        valor=data.get('valor'),
        # Converte string para objeto datetime.date com formato especificado
        data_venda=datetime.strptime(data.get('data_venda'), '%d-%m-%Y').date(),
        user_id=current_user_id
    )
    db.session.add(nova_vemda)
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
    venda.data_venda = datetime.strptime(data.get('data_venda'), '%d-%m-%Y').date()
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


@routes_bp.route('/sales/pdf', methods=['GET'])
@jwt_required()
def sales_pdf():
    start_date_str = request.args.get('start_date')
    end_date_str = request.args.get('end_date')

    start_date = datetime.strptime(start_date_str, '%d-%m-%Y')
    end_date = datetime.strptime(end_date_str, '%d-%m-%Y')

    vendas = Venda.query.filter(Venda.data_venda.between(start_date, end_date)).all()
    sales_list = [
        {
            "id": venda.id,
            "nome_cliente": venda.name_cliente,
            "produto": venda.produto,
            "valor": venda.valor,
            "data_venda": venda.data_venda.strftime('%Y-%m-%d')
        } for venda in vendas
    ]

    pdf_buffer = generate_sales_pdf(sales_list, start_date_str, end_date_str)

    return send_file(pdf_buffer, as_attachment=True, download_name='sales.pdf', mimetype='application/pdf')

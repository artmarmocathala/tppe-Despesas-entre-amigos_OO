from flask import Blueprint, request, jsonify, abort
from flask_jwt_extended import jwt_required
from database import db
from models import Compra, Imovel
from datetime import datetime


despesas_bp = Blueprint('despesas', __name__)


@despesas_bp.route(
    '/grupos/<int:grupo_id>/despesas/compras', methods=['POST']
)
@jwt_required()
def registrar_compra(grupo_id):
    data = request.get_json()
    data_str = data.get('data')
    data_dt = None
    if data_str:
        try:
            data_dt = datetime.fromisoformat(data_str)
        except ValueError:
            data_dt = datetime.strptime(data_str, '%Y-%m-%d')
    nova_compra = Compra(
        valor=data['valor'],
        data=data_dt,
        grupo_id=grupo_id,
        pagador_id=data['pagador_id'],
        nome_mercado=data.get('nome_mercado'),
        itens=data.get('itens')
    )
    db.session.add(nova_compra)
    db.session.commit()
    return jsonify(nova_compra.to_dict()), 201


@despesas_bp.route(
    '/grupos/<int:grupo_id>/despesas/imoveis', methods=['POST']
)
@jwt_required()
def registrar_despesa_imovel(grupo_id):
    data = request.get_json()
    data_str = data.get('data')
    data_dt = None
    if data_str:
        try:
            data_dt = datetime.fromisoformat(data_str)
        except ValueError:
            data_dt = datetime.strptime(data_str, '%Y-%m-%d')
    nova_despesa = Imovel(
        valor=data['valor'],
        data=data_dt,
        grupo_id=grupo_id,
        pagador_id=data['pagador_id'],
        endereco=data.get('endereco')
    )
    db.session.add(nova_despesa)
    db.session.commit()
    return jsonify(nova_despesa.to_dict()), 201


@despesas_bp.route(
    '/grupos/<int:grupo_id>/despesas', methods=['GET']
)
@jwt_required()
def listar_despesas(grupo_id):
    despesas = []
    compras = Compra.query.filter_by(grupo_id=grupo_id).all()
    imoveis = Imovel.query.filter_by(grupo_id=grupo_id).all()
    for despesa in compras + imoveis:
        despesas.append(despesa.to_dict())
    return jsonify(despesas)


@despesas_bp.route(
    '/despesas/compras/<int:compra_id>', methods=['GET']
)
@jwt_required()
def obter_compra(compra_id):
    compra = db.session.get(Compra, compra_id)
    if not compra:
        abort(404)
    return jsonify(compra.to_dict())


@despesas_bp.route(
    '/despesas/imoveis/<int:imovel_id>', methods=['GET']
)
@jwt_required()
def obter_imovel(imovel_id):
    imovel = db.session.get(Imovel, imovel_id)
    if not imovel:
        abort(404)
    return jsonify(imovel.to_dict())


@despesas_bp.route('/despesas/compras/<int:compra_id>', methods=['PUT'])
@jwt_required()
def atualizar_compra(compra_id):
    compra = db.session.get(Compra, compra_id)
    if not compra:
        abort(404, description="Compra não encontrada")

    data = request.get_json()
    compra.valor = data.get('valor', compra.valor)
    if data.get('data'):
        compra.data = datetime.fromisoformat(data.get('data'))
    compra.pagador_id = data.get('pagador_id', compra.pagador_id)
    compra.nome_mercado = data.get('nome_mercado', compra.nome_mercado)

    if 'itens' in data:
        compra.itens = data['itens']

    db.session.commit()
    return jsonify(compra.to_dict())


@despesas_bp.route('/despesas/imoveis/<int:imovel_id>', methods=['PUT'])
@jwt_required()
def atualizar_imovel(imovel_id):
    imovel = db.session.get(Imovel, imovel_id)
    if not imovel:
        abort(404, description="Despesa de imóvel não encontrada")

    data = request.get_json()
    imovel.valor = data.get('valor', imovel.valor)
    if data.get('data'):
        imovel.data = datetime.fromisoformat(data.get('data'))
    imovel.pagador_id = data.get('pagador_id', imovel.pagador_id)
    imovel.endereco = data.get('endereco', imovel.endereco)

    db.session.commit()
    return jsonify(imovel.to_dict())


@despesas_bp.route(
    '/despesas/compras/<int:compra_id>', methods=['DELETE']
)
@jwt_required()
def deletar_compra(compra_id):
    compra = db.session.get(Compra, compra_id)
    if not compra:
        abort(404)
    db.session.delete(compra)
    db.session.commit()
    return jsonify({
        'message': 'Compra deletada com sucesso.'
    }), 200


@despesas_bp.route(
    '/despesas/imoveis/<int:imovel_id>', methods=['DELETE']
)
@jwt_required()
def deletar_imovel(imovel_id):
    imovel = db.session.get(Imovel, imovel_id)
    if not imovel:
        abort(404)
    db.session.delete(imovel)
    db.session.commit()
    return jsonify({
        'message': 'Despesa de imóvel deletada com sucesso.'
    }), 200

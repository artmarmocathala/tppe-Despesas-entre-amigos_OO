from flask import Blueprint, request, jsonify, abort
from flask_jwt_extended import jwt_required, get_jwt_identity
from database import db
from models import Grupo, Pessoa, Despesa


grupos_bp = Blueprint('grupos', __name__)


@grupos_bp.route('/', methods=['POST'])
@jwt_required()
def criar_grupo():
    usuario_id = get_jwt_identity()
    data = request.get_json()
    novo_grupo = Grupo(
        nome=data['nome'],
        max_pessoas=data.get('max_pessoas'),
        usuario_id=usuario_id
    )
    db.session.add(novo_grupo)
    db.session.commit()
    return jsonify(novo_grupo.to_dict()), 201


@grupos_bp.route('/', methods=['GET'])
@jwt_required()
def listar_grupos():
    usuario_id = get_jwt_identity()
    grupos = Grupo.query.all()
    return jsonify([grupo.to_dict() for grupo in grupos])


@grupos_bp.route('/<int:grupo_id>', methods=['GET'])
@jwt_required()
def obter_grupo(grupo_id):
    grupo = db.session.get(Grupo, grupo_id)
    if not grupo:
        abort(404)
    dados_grupo = grupo.to_dict()
    dados_grupo['pessoas'] = [p.to_dict() for p in grupo.pessoas]
    dados_grupo['despesas'] = [d.to_dict() for d in grupo.despesas]
    dados_grupo['divisao'] = grupo.dividir_despesas()

    return jsonify(dados_grupo)


@grupos_bp.route('/<int:grupo_id>/divisao', methods=['GET'])
@jwt_required()
def dividir_despesas(grupo_id):
    grupo = db.session.get(Grupo, grupo_id)
    if not grupo:
        abort(404)
    return jsonify(grupo.dividir_despesas())


@grupos_bp.route('/<int:grupo_id>', methods=['PUT'])
@jwt_required()
def atualizar_grupo(grupo_id):
    grupo = db.session.get(Grupo, grupo_id)
    if not grupo:
        abort(404)
    data = request.get_json()
    grupo.nome = data.get('nome', grupo.nome)
    grupo.max_pessoas = data.get(
        'max_pessoas', grupo.max_pessoas
    )
    db.session.commit()
    return jsonify(grupo.to_dict())


@grupos_bp.route('/<int:grupo_id>', methods=['DELETE'])
@jwt_required()
def deletar_grupo(grupo_id):
    grupo = db.session.get(Grupo, grupo_id)
    if not grupo:
        abort(404)
    for despesa in grupo.despesas:
        db.session.delete(despesa)
    for pessoa in grupo.pessoas:
        db.session.delete(pessoa)
    db.session.delete(grupo)
    db.session.commit()
    return jsonify({
        'message': 'Grupo deletado com sucesso.'
    }), 200

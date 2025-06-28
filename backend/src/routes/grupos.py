from flask import Blueprint, request, jsonify, abort
from models import db, Grupo


grupos_bp = Blueprint('grupos', __name__)


@grupos_bp.route('/grupos', methods=['POST'])
def criar_grupo():
    data = request.get_json()
    novo_grupo = Grupo(
        nome=data['nome'],
        max_pessoas=data.get('max_pessoas')
    )
    db.session.add(novo_grupo)
    db.session.commit()
    return jsonify(novo_grupo.to_dict()), 201


@grupos_bp.route('/grupos', methods=['GET'])
def listar_grupos():
    grupos = Grupo.query.all()
    return jsonify([grupo.to_dict() for grupo in grupos])

@grupos_bp.route('/grupos/<int:grupo_id>', methods=['GET'])
def obter_grupo(grupo_id):
    grupo = db.session.get(Grupo, grupo_id)
    if not grupo:
        abort(404)
    return jsonify(grupo.to_dict())


@grupos_bp.route('/grupos/<int:grupo_id>', methods=['PUT'])
def atualizar_grupo(grupo_id):
    grupo = db.session.get(Grupo, grupo_id)
    if not grupo:
        abort(404)
    data = request.get_json()
    grupo.nome = data.get('nome', grupo.nome)
    grupo.max_pessoas = data.get('max_pessoas', grupo.max_pessoas)
    db.session.commit()
    return jsonify(grupo.to_dict())


@grupos_bp.route('/grupos/<int:grupo_id>', methods=['DELETE'])
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
    return jsonify({'message': 'Grupo deletado com sucesso.'}), 200

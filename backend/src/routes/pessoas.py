from flask import Blueprint, request, jsonify, abort
from flask_jwt_extended import jwt_required
from database import db
from models import Pessoa, Grupo

pessoas_bp = Blueprint('pessoas', __name__)


@pessoas_bp.route('/grupos/<int:grupo_id>/pessoas', methods=['POST'])
@jwt_required()
def adicionar_pessoa(grupo_id):
    grupo = db.session.get(Grupo, grupo_id)
    if not grupo:
        abort(404)
    data = request.get_json()
    if grupo.max_pessoas and len(grupo.pessoas) >= grupo.max_pessoas:
        return jsonify({
            'error': 'Grupo já atingiu o número máximo de pessoas'
        }), 400
    nova_pessoa = Pessoa(
        nome=data['nome'],
        cpf=data['cpf'],
        grupo_id=grupo_id
    )
    db.session.add(nova_pessoa)
    db.session.commit()
    return jsonify(nova_pessoa.to_dict()), 201


@pessoas_bp.route('/grupos/<int:grupo_id>/pessoas', methods=['GET'])
@jwt_required()
def listar_pessoas(grupo_id):
    pessoas = Pessoa.query.filter_by(grupo_id=grupo_id).all()
    return jsonify([pessoa.to_dict() for pessoa in pessoas])


@pessoas_bp.route('/pessoas/<int:pessoa_id>', methods=['GET'])
@jwt_required()
def obter_pessoa(pessoa_id):
    pessoa = db.session.get(Pessoa, pessoa_id)
    if not pessoa:
        abort(404)
    return jsonify(pessoa.to_dict())


@pessoas_bp.route('/pessoas/<int:pessoa_id>', methods=['PUT'])
@jwt_required()
def atualizar_pessoa(pessoa_id):
    pessoa = db.session.get(Pessoa, pessoa_id)
    if not pessoa:
        abort(404)
    data = request.get_json()
    pessoa.nome = data.get('nome', pessoa.nome)
    pessoa.cpf = data.get('cpf', pessoa.cpf)
    db.session.commit()
    return jsonify(pessoa.to_dict())


@pessoas_bp.route('/pessoas/<int:pessoa_id>', methods=['DELETE'])
def deletar_pessoa(pessoa_id):
    pessoa = db.session.get(Pessoa, pessoa_id)
    if not pessoa:
        abort(404)
    db.session.delete(pessoa)
    db.session.commit()
    return jsonify({
        'message': 'Pessoa deletada com sucesso.'
    }), 200

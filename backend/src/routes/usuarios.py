from flask import Blueprint, request, jsonify, abort
from database import db
from models import Usuario
from flask_jwt_extended import get_jwt_identity, get_jwt, jwt_required
from decorators import superuser_required

usuarios_bp = Blueprint('usuarios', __name__)


@usuarios_bp.route('/', methods=['POST'])
def criar_usuario():
    data = request.get_json()
    if not all(k in data for k in ('nome', 'email', 'senha')):
        return jsonify({
            'error': 'Campos obrigatórios: nome, email, senha'
        }), 400
    if Usuario.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email já cadastrado'}), 400
    usuario = Usuario(
        nome=data['nome'],
        email=data['email'],
        is_superuser=data.get('is_superuser', False)
    )
    usuario.set_senha(data['senha'])
    db.session.add(usuario)
    db.session.commit()
    return jsonify(usuario.to_dict()), 201


@usuarios_bp.route('/', methods=['GET'])
@superuser_required()
def listar_usuarios():
    usuarios = Usuario.query.all()
    return jsonify([u.to_dict() for u in usuarios])


@usuarios_bp.route('/<int:usuario_id>', methods=['GET'])
@superuser_required()
def obter_usuario(usuario_id):
    usuario = db.session.get(Usuario, usuario_id)
    if not usuario:
        abort(404)
    return jsonify(usuario.to_dict())


@usuarios_bp.route('/<int:usuario_id>', methods=['PUT'])
@jwt_required()
def atualizar_usuario(usuario_id):
    user_id = get_jwt_identity()
    claims = get_jwt()
    if not (claims.get("is_superuser") or int(user_id) == usuario_id):
        abort(403, description="Acesso negado.")
    usuario = db.session.get(Usuario, usuario_id)
    if not usuario:
        abort(404)
    data = request.get_json()
    usuario.nome = data.get('nome', usuario.nome)
    usuario.email = data.get('email', usuario.email)
    if 'senha' in data:
        usuario.set_senha(data['senha'])
    if 'is_superuser' in data:
        usuario.is_superuser = data['is_superuser']
    db.session.commit()
    return jsonify(usuario.to_dict())


@usuarios_bp.route('/<int:usuario_id>', methods=['DELETE'])
@jwt_required()
def deletar_usuario(usuario_id):
    user_id = get_jwt_identity()
    claims = get_jwt()
    if not (claims.get("is_superuser") or int(user_id) == usuario_id):
        abort(403, description="Acesso negado.")
    usuario = db.session.get(Usuario, usuario_id)
    if not usuario:
        abort(404)
    db.session.delete(usuario)
    db.session.commit()
    return jsonify({
        'message': 'Usuário deletado com sucesso.'
    }), 200


@usuarios_bp.route('/me', methods=['GET'])
@jwt_required()
def obter_me():
    user_id = get_jwt_identity()
    usuario = db.session.get(Usuario, int(user_id))
    if not usuario:
        abort(404)
    return jsonify(usuario.to_dict())

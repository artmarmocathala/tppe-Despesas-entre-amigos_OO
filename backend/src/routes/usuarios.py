from flask import Blueprint, request, jsonify, abort
from models import db, Usuario

usuarios_bp = Blueprint('usuarios', __name__)


@usuarios_bp.route('/usuarios', methods=['POST'])
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


@usuarios_bp.route('/usuarios', methods=['GET'])
def listar_usuarios():
    usuarios = Usuario.query.all()
    return jsonify([u.to_dict() for u in usuarios])


@usuarios_bp.route('/usuarios/<int:usuario_id>', methods=['GET'])
def obter_usuario(usuario_id):
    usuario = db.session.get(Usuario, usuario_id)
    if not usuario:
        abort(404)
    return jsonify(usuario.to_dict())


@usuarios_bp.route('/usuarios/<int:usuario_id>', methods=['PUT'])
def atualizar_usuario(usuario_id):
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


@usuarios_bp.route('/usuarios/<int:usuario_id>', methods=['DELETE'])
def deletar_usuario(usuario_id):
    usuario = db.session.get(Usuario, usuario_id)
    if not usuario:
        abort(404)
    db.session.delete(usuario)
    db.session.commit()
    return jsonify({
        'message': 'Usuário deletado com sucesso.'
    }), 200
